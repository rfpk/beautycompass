from django.db.models import Q, F, IntegerField, Count, Case, When
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Cast
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.utils.translation import gettext_lazy as _
from pytils.translit import slugify
from datetime import date
from apps.manufacturers.models import Manufacturer
from apps.products.mixins import ProductMixin, SeriesMixin, BrandMixin, ViewMixin

from apps.catalog.models import Category
from apps.products.forms import CommentForm, BrandBannerFormSet, BrandLinkFormSet, SeriesBannerFormSet, \
    ProductImageFormSet, ProductLinkFormSet
from apps.products.models import Review, Brand, Series, Product, ReviewImage, Tag, BrandSubscriber, \
    ProductImage, Prescription, KeyAsset, KeyAction, Format, Sex
from apps.landing.models import MainBanner
from apps.products.utils import update_product_rate
from apps.profile.models import Profile
from apps.tools.database_operations import ADD, REMOVE


def create_review(request, pk):
    if not request.user.is_authenticated:
        return redirect("landing:main_page")
    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        return JsonResponse(
            {"message": "Such profile is not exist!",
             "status": "error"}
        )
    product = Product.objects.filter(pk=pk).first()
    if not product:
        return JsonResponse(
            {"message": "Such product is not exist!",
             "status": "error"}
        )
    if product.brand.manufacturer.profile == profile:
        return JsonResponse(
            {"message": "Forbidden to leave a review about your own product!",
             "status": "error"}
        )
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            review = form.save(commit=False)
            review.profile = profile
            review.product = product
            review.save()

            # Save Images
            for image in images:
                ReviewImage.objects.create(review=review, image=image)

            product.rating = update_product_rate(product)
            product.save()
            return redirect("products:product_reviews", slug=product.slug)
        else:
            return JsonResponse(
                {"message": "The data is incorrect", "status": "error"}
            )


class ProductQuestionsView(ListView):
    model = Review
    template_name = 'product/product_questions.html'
    context_object_name = 'questions'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product.objects.select_related('series'), slug=self.kwargs['slug'])
        self.object_list = (product.product_questions.select_related('profile').
                            prefetch_related('question_answers', 'question_answers__manufacturer')
                            .annotate(author_id=F('profile__profile_author__id')))
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        context = self.get_context_data()
        context['product'] = product
        return self.render_to_response(context)


def get_reviews(request):
    review_id = request.GET.get('id')

    review = (Review.objects
               .all()
               .select_related('product', 'profile')
               .prefetch_related('review_answers')
               .annotate(
                   answer_text=F('review_answers__text'),
                   answer_created_at=F('review_answers__created_at'),
                   answer_manufacturer_name=F('review_answers__manufacturer__name'),
               )
               .annotate(review_rating_normalized=F('rating') / 5 * 100)
               .annotate(review_rating_int=Cast('review_rating_normalized', IntegerField()))
               .annotate(product_rating_normalized=F('product__rating') / 5 * 100)
               .annotate(product_rating_int=Cast('product_rating_normalized', IntegerField()))
               .annotate(author_id=F('profile__profile_author__id'))
              ).filter(pk=int(review_id)).first()
    data = {
        'author_id': review.author_id,
        'avatar': review.profile.avatar.url if review.profile.avatar else '',
        'first_name': review.profile.first_name,
        'last_name': review.profile.last_name[0:1],
        'review_rating_int': review.review_rating_int,
        'created_at': review.created_at.strftime('%d.%m.%Y'),
        'text': review.text,
        'answer_date': review.answer_created_at.strftime('%d.%m.%Y') if review.answer_created_at else None,
        'answer_text': review.answer_text,
        'answer_manufacturer_name': review.answer_manufacturer_name,
    }
    return JsonResponse({'data': data}, status=200)


def get_tags(request, slug, word):
    tags = Product.objects.filter(
        Q(category__slug=slug) &
        Q(tag__name__icontains=word),
    ).distinct('tag__name').values('tag__name', 'tag__slug')

    html = render_to_string('utils/tags_for.html', {'data': tags, 'word': word})
    return HttpResponse(html)

class ProductPhotosView(ListView):
    model = ReviewImage
    template_name = 'product/product_photos.html'
    context_object_name = 'review'
    paginate_by = 42

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']

        context = super(ProductPhotosView, self).get_context_data(**kwargs)
        context['photos'] = (ReviewImage.objects
                             .filter(review__product__slug=slug, review__is_publish=True)
                             .select_related('review', 'review__product')
                             .order_by('review__pk')
                            )

        context['review'] = (Review.objects
                            .filter(
                                is_publish=True,
                                product__slug=slug,
                                pk__in=context['photos'].values_list('review__pk', flat=True)
                            )
                            .select_related('product', 'product__series')
                            .prefetch_related('review_answers')
                            .annotate(
                                 answer_text=F('review_answers__text'),
                                 answer_date=F('review_answers__created_at'),
                                 answer_manufacturer_logo=F('review_answers__manufacturer__logo'),
                                 answer_manufacturer_name=F('review_answers__manufacturer__name'),
                            )
                            .annotate(author_id=F('profile__profile_author__id'))
                            .annotate(review_rating_normalized=F('rating') / 5 * 100)
                            .annotate(review_rating_int=Cast('review_rating_normalized', IntegerField()))
                            .order_by('pk')
                            .first())
        return context


class ProductReviewsView(ListView):
    model = Review
    template_name = 'product/product_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 5

    def get_queryset(self):
        return (Review.objects
                .filter(product__slug=self.kwargs['slug'], is_publish=True)
                .select_related('profile', 'product', 'product__brand__manufacturer')
                .prefetch_related('images', 'review_answers')
                .annotate(
                    answer_text=F('review_answers__text'),
                    answer_date=F('review_answers__created_at'),
                    answer_manufacturer_logo=F('review_answers__manufacturer__logo'),
                    answer_manufacturer_name=F('review_answers__manufacturer__name'),
                )
                .annotate(author_id=F('profile__profile_author__id'))
                .annotate(rating_normalized=F('rating') / 5 * 100)
                .annotate(rating_int=Cast('rating_normalized', IntegerField()))
                .annotate(likes_count=Count(Case(When(reaction__type_action=1, then=1))),
                         dislikes_count=Count(Case(When(reaction__type_action=0, then=1))))
                )

    def get_context_data(self, **kwargs):
        context = super(ProductReviewsView, self).get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product.objects.select_related('series'), slug=self.kwargs['slug'])
        return context


class ProductDetailReviewView(DetailView):
    model = Review
    template_name = 'product/product_review_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailReviewView, self).get_context_data(**kwargs)
        context['review'] = (Review.objects.filter(pk=self.kwargs['pk'], is_publish=True).
                             annotate(rating_normalized=F('rating') / 5 * 100).
                             annotate(rating_int=Cast('rating_normalized', IntegerField())).first())

        context['product'] = context['review'].product
        context['answer'] = context['review'].review_answers.select_related('manufacturer').first()
        context['review_images'] = context['review'].images.all()
        context['product_reviews_images'] = ReviewImage.objects.filter(review__product=context['product'])
        return context


class BrandCreateView(LoginRequiredMixin, BrandMixin, CreateView):

    def get_context_data(self, **kwargs):
        context = super(BrandCreateView, self).get_context_data(**kwargs)
        context['brand_banner_formset'] = BrandBannerFormSet()
        context['brand__link__formset'] = BrandLinkFormSet()
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        brand_banner_formset = BrandBannerFormSet(prefix="brand_banners")
        brand_link_formset = BrandLinkFormSet(prefix='brand_links')

        return render(request,'product/brand_detail_info.html', {
            'form': form,
            'brand_banner_formset': brand_banner_formset,
            'brand_link_formset': brand_link_formset,
        })

    def post(self, request, *args, **kwargs):
        self.object = None
        manufacturer = get_object_or_404(Manufacturer, profile__user=request.user)
        self.check_manufacturer_status(manufacturer)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        brand_banner_formset = BrandBannerFormSet(self.request.POST, request.FILES, prefix="brand_banners")
        brand_link_formset = BrandLinkFormSet(self.request.POST, prefix="brand_links")
        if form.is_valid() and brand_banner_formset.is_valid() and brand_link_formset.is_valid():
            brand = form.save(commit=False)
            brand.manufacturer = manufacturer
            brand.slug = slugify(brand.name)
            brand.save()

            tags = request.POST.getlist('tag', None)
            if tags:
                tags = Tag.objects.filter(pk__in=tags)
                brand = Brand.objects.filter(id=brand.id).first()
                brand.tag.set(tags)
                brand.save()


            # Добавление Ссылок
            for form in brand_link_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.name and instance.url:
                                instance.brand = brand
                                instance.save()

            # Сохранение баннеров
            for form in brand_banner_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.banner and instance.url:
                                instance.brand = brand
                                instance.save()
            return redirect('products:change_brand', slug=brand.slug)
        else:
            return JsonResponse({
                'status': 'error', 'message': 'The data is incorrect'
            })


def delete_brand(request, slug):
    user = request.user
    is_auth = user.is_authenticated

    if not is_auth:
        return redirect("/")

    brand = get_object_or_404(Brand, slug=slug, manufacturer__profile__user=user)
    brand.delete()
    return redirect('profile:profile_detail')

class BrandUpdateView(LoginRequiredMixin, BrandMixin, UpdateView):
    model = Brand
    context_object_name = 'brand'

    def get_object(self, queryset=None):
        return get_object_or_404(Brand, slug=self.kwargs['slug'], manufacturer__profile__user=self.request.user)

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        brand_object = self.get_object()

        tags = brand_object.tag.all()

        return render(request, 'product/brand_detail_info.html', {
            'form': form_class(instance=brand_object),
            'brand_banner_formset': BrandBannerFormSet(prefix="brand_banners", instance=brand_object),
            'brand_link_formset': BrandLinkFormSet(prefix='brand_links', instance=brand_object),
            'tags_name': list(tags.values_list('name', flat=True)),
            'brand': brand_object,
        })

    def post(self, request, *args, **kwargs):
        self.object = None
        manufacturer = get_object_or_404(Manufacturer, profile__user=request.user)
        if self.get_object().manufacturer != manufacturer:
            return JsonResponse(
                {
                    "message": "Current manufacturer user can't update not self brand object",
                    "status": "error"
                }
            )
        self.check_manufacturer_status(manufacturer)
        form_class = self.get_form_class()
        form = form_class(self.request.POST, request.FILES, instance=self.get_object())
        brand_banner_formset = BrandBannerFormSet(self.request.POST, request.FILES,
                                                  instance=self.get_object(), prefix="brand_banners")
        brand_link_formset = BrandLinkFormSet(self.request.POST, instance=self.get_object(),
                                              prefix="brand_links")
        if form.is_valid() and brand_banner_formset.is_valid() and brand_link_formset.is_valid():
            tags = request.POST.getlist('tag', [])

            brand = form.save(commit=False)
            brand.slug = slugify(brand.name)
            if tags:
                tags = Tag.objects.filter(pk__in=tags)
                brand.tag.set(tags)
            brand.save()

            # Добавление Ссылок
            for form in brand_link_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.name and instance.url:
                                instance.brand = self.get_object()
                                instance.save()

            # Сохранение баннеров
            for form in brand_banner_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.banner and instance.url:
                                instance.brand = self.get_object()
                                instance.save()

            return redirect('products:change_brand', slug=slugify(brand.name))
        else:
            return JsonResponse({'status': 'error', 'message': 'The data is incorrect'})


class SeriesCreateView(LoginRequiredMixin, SeriesMixin, CreateView):

    def get_object(self, queryset=None):
        return get_object_or_404(Brand, slug=self.kwargs['slug'], manufacturer__profile__user=self.request.user)

    def get(self, request, *args, **kwargs):
        brand = self.get_object()
        form_class = self.get_form_class()
        form = form_class(user=request.user)
        formset = SeriesBannerFormSet(prefix="series_banners")

        return render(request, 'product/create_series.html', {
            'form': form,
            'series_banner_formset': formset,
            'brand': brand
        })

    def post(self, request, *args, **kwargs):
        self.object = None
        manufacturer = get_object_or_404(Manufacturer, profile__user=request.user)
        self.check_manufacturer_status(manufacturer)

        form_class = self.get_form_class()
        form = form_class(
            self.request.POST,
            self.request.FILES,
            user=self.request.user,
        )
        series_banner_formset = SeriesBannerFormSet(self.request.POST, request.FILES, prefix="series_banners")
        if form.is_valid() and series_banner_formset.is_valid():
            tags = request.POST.getlist('tag', [])

            series = form.save()
            series.slug = slugify(series.name)
            if tags:
                tags = Tag.objects.filter(pk__in=tags)
                series.tag.set(tags)
            series.save()

            for form in series_banner_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.banner and instance.url:
                                instance.series = series
                                instance.save()
            return redirect("products:change_series", slug=slugify(series.name))
        else:
            return JsonResponse({'status': 'error', 'message': 'The data is incorrect'})


def delete_series(request, slug):
    user = request.user
    is_auth = user.is_authenticated

    if not is_auth:
        return redirect("/")

    series = get_object_or_404(Series, slug=slug, brand__manufacturer__profile__user=user)
    series.delete()
    return redirect('profile:profile_detail')


class SeriesUpdateView(LoginRequiredMixin, SeriesMixin, UpdateView):
    model = Series

    def get_context_data(self, **kwargs):
        context = super(SeriesUpdateView, self).get_context_data(**kwargs)
        context['series_banner_formset'] = SeriesBannerFormSet()
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Series, slug=self.kwargs['slug'], brand__manufacturer__profile__user=self.request.user)

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        series_object = self.get_object()

        formset = SeriesBannerFormSet(
            prefix="series_banners",
            instance=series_object,
        )

        tags = series_object.tag.all()

        return render(request, 'product/create_series.html', {
            'form': form_class(instance=series_object, user=self.request.user),
            'series_banner_formset': formset,
            'series': series_object,
            'tags_name': list(tags.values_list('name', flat=True))
        })

    def post(self, request, *args, **kwargs):
        self.object = None

        manufacturer = get_object_or_404(
            Manufacturer,
            profile__user=request.user
        )
        if self.get_object().brand.manufacturer != manufacturer:
            return JsonResponse(
                {
                    "message": "Current manufacturer user can't update not self brand object",
                    "status": "error"
                }
            )
        self.check_manufacturer_status(manufacturer)
        form_class = self.get_form_class()

        form = form_class(
            self.request.POST,
            self.request.FILES,
            user=self.request.user,
            instance=self.get_object(),
        )
        series_banner_formset = SeriesBannerFormSet(
            self.request.POST,
            self.request.FILES,
            prefix="series_banners",
            instance=self.get_object(),
        )
        if form.is_valid() and series_banner_formset.is_valid():
            tags = request.POST.getlist('tag', [])

            series = form.save(commit=False)
            series.name = self.get_object().name
            if tags:
                tags = Tag.objects.filter(pk__in=tags)
                series.tag.set(tags)
            series.save()

            for form in series_banner_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.banner and instance.url:
                                instance.series = self.get_object()
                                instance.save()

            return redirect("products:change_series", slug=self.get_object().slug)
        else:
            return JsonResponse({'status': 'error', 'message': 'The data is incorrect'})



class ListBrandView(ListView):
    model = Brand
    template_name = 'brand/list_brands.html'
    context_object_name = 'brands'
    paginate_by = 5

    def get_queryset(self):
        return (Brand.objects.filter(manufacturer__manufacturer_tariffs__end_date__gte=date.today()).
                select_related('manufacturer', 'manufacturer__profile', 'country').prefetch_related('tag'))


def sort_products_date(request):
    sort = request.GET.get('newest', 'oldest')
    products = Product.objects.filter(brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today())
    if sort == 'oldest':
        products = products.order_by('created_at').values()
    else:
        products = products.order_by('-created_at').values()
    return JsonResponse(
        {'products': list(products)}
    )


class ProductFilterView(ListView):
    model = Product
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        sex = request.GET.getlist('sex[]')
        format = request.GET.getlist('format[]')
        category = request.GET.getlist('category')
        country = request.GET.getlist('country[]')
        key_asset = request.GET.getlist('key_asset[]')
        key_action = request.GET.getlist('key_action[]')
        prescription = request.GET.getlist('prescription[]')
        price_category = request.GET.getlist('price_category[]')
        age_recommendation = request.GET.getlist('age_recommendation[]')
        sort_by = request.GET.get('sortBy', 'created_at')

        q_objects = Q()

        if format: q_objects &= Q(format__slug__in=format)
        if price_category: q_objects &= Q(price_category__slug__in=price_category)
        if prescription: q_objects &= Q(prescription__slug__in=prescription)
        if key_asset: q_objects &= Q(key_asset__slug__in=key_asset)
        if key_action: q_objects &= Q(key_action__slug__in=key_action)
        if sex: q_objects &= Q(sex__slug__in=sex)
        if age_recommendation: q_objects &= Q(age_recommendation__slug__in=age_recommendation)

        products = Product.objects.filter(
            Q(brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today()) &
            Q(category__slug__in=category) &
            q_objects
        ).order_by(sort_by)

        return JsonResponse({'data': list(products.values())}, status=200)


class TagProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/list_product.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(tag__slug=self.kwargs['tag_slug'],
                                      brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today())


def delete_product(request, slug):
    user = request.user
    is_auth = user.is_authenticated

    if not is_auth:
        return redirect("/")

    product = get_object_or_404(Product, slug=slug, brand__manufacturer__profile__user=user)
    product.delete()
    return redirect('profile:profile_detail')


class ProductCreateView(LoginRequiredMixin, ProductMixin, CreateView):
    
    def get_brand(self):
        return get_object_or_404(Brand, slug=self.kwargs['brand_slug'], manufacturer__profile__user=self.request.user)
    
    def get_series(self):
        return get_object_or_404(Series, slug=self.kwargs['series_slug'], brand__manufacturer__profile__user=self.request.user)
    
    def check_objects(self):
        return self.get_brand(), self.get_series()

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['product_image_formset'] = ProductImageFormSet()
        context['product_link_formset'] = ProductLinkFormSet()
        return context

    def get(self, request, *args, **kwargs):
        brand, series = self.check_objects()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        product_image_formset = ProductImageFormSet(prefix="product_images")
        product_link_formset = ProductLinkFormSet(prefix="product_links")
        categories = (Category.objects
                      .filter(parent=None)
                      .select_related('parent')
                      .prefetch_related('children', 'children__children')
                      .annotate(count=Count('children'))
                      ).order_by('-count')
        return render(request, 'product/product_detail_info.html', {
            'form': form,
            'product_image_formset': product_image_formset,
            'product_link_formset': product_link_formset,
            'categories': categories,
            'brand': brand,
            'series': series,
        })

    def post(self, request, *args, **kwargs):
        self.object = None
        manufacturer = get_object_or_404(Manufacturer, profile__user=request.user)
        manufacturer_current_tariff = manufacturer.manufacturer_tariffs
        manufacturer_current_tariff_last = manufacturer_current_tariff.last()
        self.check_manufacturer_status(manufacturer)
        manufacturer_product_count = Product.objects.filter(series__brand__manufacturer=manufacturer).count()
        if manufacturer_product_count > manufacturer_current_tariff_last.tariff_plan.type.quantity:
            return JsonResponse(
                {
                    "message": "Quantity of publish products can't be more of quantity current tariff!",
                    "status": "error"
                }
            )
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        product_image_formset = ProductImageFormSet(self.request.POST, request.FILES, prefix="product_images")
        product_link_formset = ProductLinkFormSet(self.request.POST, prefix="product_links")
        if form.is_valid() and product_image_formset.is_valid() and product_link_formset.is_valid():
            brand = manufacturer.manufacturer_brands.all().first()
            series = brand.series.all().first()

            categories = request.POST.getlist('categories', [])
            prescriptions = request.POST.getlist('prescriptions', [])
            key_assets = request.POST.getlist('key_assets', [])
            key_actions = request.POST.getlist('key_actions', [])
            format = request.POST.getlist('formats', [])
            sex = request.POST.get('sex', None)
            categories = Category.objects.filter(name__in=categories)
            prescriptions = Prescription.objects.filter(name__in=prescriptions)
            key_assets = KeyAsset.objects.filter(name__in=key_assets)
            key_actions = KeyAction.objects.filter(name__in=key_actions)
            format = Format.objects.filter(name__in=format)
            sex = Sex.objects.filter(pk=sex)

            product = form.save(commit=False)
            product.slug = slugify(product.name)
            product.brand = brand
            product.series = series
            product.save()

            if categories:
                product.category.set(categories)
            if prescriptions:
                product.prescription.set(prescriptions)
            if key_assets:
                product.key_asset.set(key_assets)
            if key_actions:
                product.key_action.set(key_actions)
            if format:
                product.format = format.first()
            if sex:
                product.sex.set(sex)

            product.save()

            # Добавление фотографий
            for form in product_image_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.image:
                                number = request.POST.get(f'{form.prefix}-number', None)
                                try:
                                    if number and isinstance(int(number), int) and number == '1':
                                        product.thumbnail = instance.image
                                        product.save()
                                    else:
                                        instance.product = product
                                        instance.save()
                                except ValueError:
                                    instance.product = product
                                    instance.save()

            # Добавление Ссылок
            for form in product_link_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.name and instance.url:
                                instance.product = product
                                instance.save()

            return redirect('products:change_product', slug=product.slug)
        else:
            return JsonResponse({'status': 'error', 'message': 'The data is incorrect'})


class ProductUpdateView(LoginRequiredMixin, ProductMixin, UpdateView):
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['product_image_formset'] = ProductImageFormSet()
        context['product_link_formset'] = ProductLinkFormSet()
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs['slug'], brand__manufacturer__profile__user=self.request.user)

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        product_object = self.get_object()
        categories = (Category.objects
                        .filter(parent=None)
                        .select_related('parent')
                        .prefetch_related('children', 'children__children')
                        .annotate(count=Count('children'))
                    ).order_by('-count')

        categories_user = product_object.category.all()
        prescription_user = product_object.prescription.all()
        key_asset_user = product_object.key_asset.all()
        key_action_user = product_object.key_action.all()
        format_user = product_object.format
        sex_user = product_object.sex.all()

        return render(request, 'product/product_detail_info.html', {
            'form': form_class(instance=product_object),
            'product_image_formset': ProductImageFormSet(prefix="product_images", instance=product_object),
            'product_link_formset': ProductLinkFormSet(prefix="product_links", instance=product_object),
            'categories': categories,
            'categories_user': categories_user.values_list('name', flat=True),
            'prescriptions_user': list(prescription_user.values_list('name', flat=True)),
            'key_assets_user': list(key_asset_user.values_list('name', flat=True)),
            'key_actions_user': list(key_action_user.values_list('name', flat=True)),
            'sex_user': list(sex_user.values_list('name', flat=True)),
            'format_user': format_user.name if format_user else '',
            'product': product_object,
        })


    def post(self, request, *args, **kwargs):
        manufacturer = get_object_or_404(Manufacturer, profile__user=request.user)
        product_object = self.get_object()
        if product_object.brand.manufacturer != manufacturer:
            return JsonResponse(
                {
                    "message": "Current manufacturer user can't update not self product object",
                    "status": "error"
                }
            )
        self.check_manufacturer_status(manufacturer)
        form_class = self.get_form_class()
        form = form_class(self.request.POST, request.FILES, instance=self.get_object())
        product_image_formset = ProductImageFormSet(self.request.POST, request.FILES,
                                                    instance=product_object, prefix="product_images")
        product_link_formset = ProductLinkFormSet(self.request.POST, instance=product_object,
                                                  prefix="product_links")
        if form.is_valid() and product_image_formset.is_valid() and product_link_formset.is_valid():
            series = self.get_object().series
            categories = request.POST.getlist('categories', [])
            prescriptions = request.POST.getlist('prescriptions', [])
            key_assets = request.POST.getlist('key_assets', [])
            key_actions = request.POST.getlist('key_actions', [])
            format = request.POST.getlist('formats', [])
            sex = request.POST.get('sex', None)

            categories = Category.objects.filter(name__in=categories)
            prescriptions = Prescription.objects.filter(name__in=prescriptions)
            key_assets = KeyAsset.objects.filter(name__in=key_assets)
            key_actions = KeyAction.objects.filter(name__in=key_actions)
            format = Format.objects.filter(name__in=format)
            sex = Sex.objects.filter(pk=sex)

            product = form.save(commit=False)

            if categories: product.category.set(categories)
            if prescriptions: product.prescription.set(prescriptions)
            if key_assets: product.key_asset.set(key_assets)
            if key_actions: product.key_action.set(key_actions)
            if format: product.format = format.first()
            if sex: product.sex.set(sex)
            product.series = series

            form.save()

            # Добавление фотографий
            for form in product_image_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.image:
                                instance.product = self.get_object()
                                instance.save()

            # Добавление Ссылок
            for form in product_link_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.name and instance.url:
                                instance.product = self.get_object()
                                instance.save()
        return redirect('products:change_product', slug=product_object.slug)


class ProductDetailView(DetailView, ViewMixin):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Product.objects
            .select_related('series', 'brand', 'price_category')
            .prefetch_related('category')
            .annotate(rating_product=F('rating') / 5 * 100)
            .annotate(product_rating_int=Cast('rating_product', IntegerField())),
            slug=self.kwargs.get(self.slug_url_kwarg),
            brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today()
        )

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        self.check_view_user(request, self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.object

        # Reviews
        context['product_reviews_images'] = (ReviewImage.objects
                                             .filter(review__product=product, review__is_publish=True)
                                             .select_related('review'))
        context['product_reviews'] = (product.reviews
                                        .filter(is_publish=True)
                                        .select_related('product', 'profile', 'product__brand__manufacturer')
                                        .prefetch_related('review_answers', 'images')
                                        .annotate(
                                            answer_text=F('review_answers__text'),
                                            answer_date=F('review_answers__created_at'),
                                            answer_manufacturer_logo=F('review_answers__manufacturer__logo'),
                                            answer_manufacturer_name=F('review_answers__manufacturer__name'),
                                        )
                                        .annotate(review_rating_normalized=F('rating') / 5 * 100)
                                        .annotate(review_rating_int=Cast('review_rating_normalized', IntegerField()))
                                        .annotate(product_rating_normalized=F('product__rating') / 5 * 100)
                                        .annotate(product_rating_int=Cast('product_rating_normalized', IntegerField()))
                                        .order_by('-pk', '-review_answers__created_at')
                                     ).distinct('pk')
        # Questions
        context['product_questions'] = (product.product_questions
                                            .all()
                                            .select_related('profile', 'product__series__brand__manufacturer__profile')
                                            .annotate(
                                                answer_text=F('question_answers__text'),
                                                answer_date=F('question_answers__date'),
                                                answer_manufacturer_name=F('question_answers__manufacturer__name'),
                                            )
                                            .annotate(product_rating_normalized=F('product__rating') / 5 * 100)
                                            .annotate(product_rating_int=Cast('product_rating_normalized', IntegerField()))
                                            .order_by('-pk', '-date', '-question_answers__date')
                                        ).distinct('pk')
        # Images
        context['product_images'] = ProductImage.objects.filter(product=product).select_related('product')

        # Banners
        context['selection_banners'] = MainBanner.objects.filter(banner_selection=True)

        # First Category
        context['first_category'] = product.category.first()
        return context


class BrandDetailView(DetailView, ViewMixin):
    model = Brand
    template_name = 'product/catalog_brand_detail.html'
    context_object_name = 'brand'

    def get_object(self, queryset=None):
        return get_object_or_404(Brand.objects
                                    .select_related('manufacturer', 'manufacturer__profile__user'),
                                    manufacturer__manufacturer_tariffs__end_date__gte=date.today(),
                                    slug=self.kwargs.get(self.slug_url_kwarg)
                                 )

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        self.check_view_user(request, self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super(BrandDetailView, self).get_context_data(**kwargs)
        brand = self.get_object()
        context['brand_series'] = brand.series.all().prefetch_related('tag', 'products')
        context['brand_social_links'] = (brand.brand_social_links
                                            .all()
                                            .select_related('social_web')
                                            .annotate(social_logo=F('social_web__logo'))
                                        )
        context['brand_banners'] = brand.brand_banners.all()
        context['author'] = brand.manufacturer.profile.user
        return context


class BrandArticlesView(DetailView):
    model = Brand
    template_name = 'brand/brand_articles.html'

    def get_context_data(self, **kwargs):
        context = super(BrandArticlesView, self).get_context_data(**kwargs)
        brand = self.get_object()
        context['brand_articles'] = (brand.brand_articles.filter(is_publish=True, is_draft=False).select_related(
            'manufacturer', 'manufacturer__profile'))
        return context


class SeriesDetailView(DetailView, ViewMixin):
    model = Series
    template_name = 'product/catalog_series_detail.html'
    context_object_name = 'series'

    def get_object(self, queryset=None):
        return get_object_or_404(Series.objects.select_related('brand__manufacturer'),
                                    brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today(),
                                    slug=self.kwargs.get(self.slug_url_kwarg)
                                )

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        self.check_view_user(request, self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        series = self.get_object()
        context['series_products'] = (series.products
                                        .filter(brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today())
                                        .annotate(rating_normalized=F('rating') / 5 * 100)
                                        .annotate(rating_int=Cast('rating_normalized', IntegerField()))
                                     )[:15]

        context['series_banners'] = series.series_banners.all()
        return context


def brand_subscribe(request, slug):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    profile = get_object_or_404(Profile, user=request.user)
    brand = get_object_or_404(Brand, slug=slug)
    if brand.manufacturer.profile == profile:
        return JsonResponse(
            {
                "message": 'Can not to subscribe on yourself account!',
                "status": "error"
            }
        )
    last_object_action = BrandSubscriber.objects.filter(brand=brand, profile=profile).last()
    if last_object_action and last_object_action.type_action == ADD:
        type_action = REMOVE
    else:
        type_action = ADD
    new_object_action = BrandSubscriber.objects.create(brand=brand, profile=profile, type_action=type_action)

    return JsonResponse(
        {
            "message": 'Action successfully set!',
            "new_status": new_object_action.type_action,
            "status": "success"
        }
    )
