from django.db.models import F, Q, IntegerField, Count
from django.db.models.functions import Cast
from django.http import Http404
from django.views.generic import ListView
from datetime import date
from apps.catalog.models import Category
from apps.products.models import Product, PriceCategory, Prescription, KeyAsset, KeyAction, Sex, Format, \
    AgeRecommendation


class CatalogView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'catalog/catalog.html'

    def get_queryset(self):
        return (Category.objects
                    .filter(parent=None)
                    .select_related('parent')
                    .prefetch_related('children', 'children__children')
                    .annotate(count=Count('children'))
                ).order_by('-count')


class CategoryProductView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalog/catalog_filters.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        sorting_by = [
            { 'value': 'created_at', 'text': 'Сначала новые' },
            { 'value': '-created_at', 'text': 'Сначала старые' },
            { 'value': 'name', 'text': 'По названию (А-Я)' },
            { 'value': '-name', 'text': 'По названию (Я-А)' }
        ]

        prod_slug = self.kwargs.get('prod_slug')
        sub_slug = self.kwargs.get('sub_slug')
        cat_slug = self.kwargs.get('cat_slug')
        slug = prod_slug or sub_slug or cat_slug

        # Sorting Data
        sex = self.request.GET.getlist('sex')
        format = self.request.GET.getlist('format')
        country = self.request.GET.getlist('country')
        key_asset = self.request.GET.getlist('key_asset')
        key_action = self.request.GET.getlist('key_action')
        prescription = self.request.GET.getlist('prescription')
        price_category = self.request.GET.getlist('price_category')
        age_recommendation = self.request.GET.getlist('age_recommendation')
        sort_by = self.request.GET.get('sort_by', 'created_at')
        tag = self.request.GET.get('tag')
        series = self.request.GET.get('series')

        q_objects = Q()

        if format: q_objects &= Q(format__slug__in=format)
        if price_category: q_objects &= Q(price_category__slug__in=price_category)
        if prescription: q_objects &= Q(prescription__slug__in=prescription)
        if key_asset: q_objects &= Q(key_asset__slug__in=key_asset)
        if key_action: q_objects &= Q(key_action__slug__in=key_action)
        if sex: q_objects &= Q(sex__slug__in=sex)
        if age_recommendation: q_objects &= Q(age_recommendation__slug__in=age_recommendation)
        if tag: q_objects &= Q(tag__slug=tag)
        if sort_by not in [el['value'] for el in sorting_by]:
            sort_by = 'created_at'

        q_object_slug = Q()
        if slug == 'series' and series:
            q_object_slug &= Q(series__slug=series)
        else:
            q_object_slug & Q(category__slug=slug)

        self.object_list = (Product.objects
                                .filter(
                                    q_object_slug &
                                    Q(brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today()) &
                                    q_objects
                                ).order_by(sort_by)
                                .annotate(rating_normalized=F('rating') / 5 * 100)
                                .annotate(rating_int=Cast('rating_normalized', IntegerField()))
                                )

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
        context['category'] = (Category.objects.filter(slug=slug).select_related('parent').
                           prefetch_related('children', 'children__parent')).first()
        context['formats'] = Format.objects.all()
        context['price_categories'] = PriceCategory.objects.all()
        context['prescriptions'] = Prescription.objects.all()
        context['key_assets'] = KeyAsset.objects.all()
        context['key_actions'] = KeyAction.objects.all()
        context['sex'] = Sex.objects.all()
        context['age_recommendation'] = AgeRecommendation.objects.all()
        context['sortings_by'] = sorting_by

        return self.render_to_response(context)