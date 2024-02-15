
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import F, IntegerField, Q
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.forms import formset_factory

from apps.blog.models import Article, ArticleComment
from apps.manufacturers.forms import ManufacturerForm, ManufacturerMailForm, ManufacturerBannerFormSet, \
    ManufacturerLinkFormSet, MailingEmailFormSet, MailingPhoneFormSet, ManufacturerUpdateForm
from apps.manufacturers.models import Manufacturer, ManufacturerQuestionAnswer, AnswerReview, ManufacturerMailing
from apps.manufacturers.services.statistic_operations import get_likes_statistic_data, get_favorites_statistic_data, \
    get_statistic_model_data, get_statistic_links_data, get_reviews_statistic_data
from apps.products.mixins import ManufacturerStatus
from apps.products.models import Review
from apps.profile.models import Profile, ViewAction, Conversion, Question
from apps.tools.utils import filter_data


class ManufacturerCreate(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        formset_banners = ManufacturerBannerFormSet(
            prefix='manufacturer_banners'
        )
        formset_links = ManufacturerLinkFormSet(
            prefix='manufacturer_links'
        )
        form = ManufacturerForm()

        return render(request, 'manufacturer/manufacturer_profile_info.html', {
            'form': form,
            'manufacturer_banner_formset': formset_banners,
            'manufacturer_links_formset': formset_links,
        })

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=self.request.user).first()
        if not profile:
            return JsonResponse(
                {"message": "Such profile not found", "status": "error"}
            )
        form = ManufacturerForm(request.POST, request.FILES)
        manufacturer_banner_formset = ManufacturerBannerFormSet(
            request.POST,
            request.FILES,
            prefix='manufacturer_banners',
        )
        manufacturer_links_formset = ManufacturerLinkFormSet(
            request.POST,
            request.FILES,
            prefix='manufacturer_links',
        )
        if form.is_valid() and manufacturer_banner_formset.is_valid() and manufacturer_links_formset.is_valid():
            manufacturer = form.save(commit=False)
            manufacturer.profile = profile
            manufacturer.save()

            # Добавление Ссылок
            for form in manufacturer_links_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.name and instance.url:
                                instance.manufacturer = manufacturer
                                instance.save()

            # # Добавление Баннера
            for form in manufacturer_banner_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.banner and instance.url:
                                instance.manufacturer = manufacturer
                                instance.save()

            return redirect('manufacturer:change_manufacturer')
        else:
            return JsonResponse(
                {"message": "The data is incorrect", "status": "error"}
            )


class ManufacturerProfile(DetailView):
    model = Manufacturer
    template_name = 'manufacturer/manufacturer_profile.html'
    context_object_name = 'manufacturer'

    def get_paginator(self, paginate_by: int = 6):
        articles = (self.object.manufacturer_articles
                    .filter(is_publish=True, is_draft=False, is_active=True)
                    .order_by('created_at'))
        paginator = Paginator(articles, paginate_by)
        page = self.request.GET.get('page')
        page = page if page else 1
        
        try:
            data = paginator.page(page)
        except (InvalidPage, EmptyPage):
            data = paginator.page(paginator.num_pages)

        return data

    def get_context_data(self, **kwargs):
        context = super(ManufacturerProfile, self).get_context_data(**kwargs)
        context['manufacturer_social_links'] = self.object.manufacturer_social_links.all().select_related('social_web')
        context['manufacturer_articles'] = self.get_paginator()
        context['manufacturer_banners'] = self.object.manufacturer_banners.all()
        return context

    def post(self, request):
        page_no = request.POST.get('page_no', None)
        obj_paginator = self.get_paginator()
        results = list(obj_paginator.page(page_no).object_list)
        return JsonResponse({"results": results})



def change_profile_manufacturer(request):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    profile = Manufacturer.objects.filter(profile__user=request.user).first()
    if not profile:
        return JsonResponse(
            {"message": "Such profile not found", "status": "error"}
        )
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, request.FILES, instance=profile)
        manufacturer_banner_formset = ManufacturerBannerFormSet(
            request.POST,
            request.FILES,
            prefix='manufacturer_banners',
            instance=profile,
        )
        manufacturer_links_formset = ManufacturerLinkFormSet(
            request.POST,
            request.FILES,
            prefix='manufacturer_links',
            instance=profile,
        )
        if form.is_valid() and manufacturer_banner_formset.is_valid() and manufacturer_links_formset.is_valid():
            # if len(form.cleaned_data['link_shops']) + len(profile.manufacturer_links.all()) > 7:
            #     return JsonResponse(
            #         {
            #             "message": "The number of links should not exceed seven",
            #             "status": "error"
            #         }
            #     )
            
            profile = Manufacturer.objects.filter(profile__user=request.user).first()
            instance = form.save(commit=False)
            instance.profile = profile.profile
            instance.save()
            
            # Добавление Ссылок
            for form in manufacturer_links_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.name and instance.url:
                                instance.manufacturer = profile
                                instance.save()
                            
            
            # # Добавление Баннера
            for form in manufacturer_banner_formset:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        if form.instance.pk:
                            form.save()
                        else:
                            instance = form.save(commit=False)
                            if instance.banner and instance.url:
                                instance.manufacturer = profile
                                instance.save()
            return redirect("manufacturer:change_manufacturer")
        else:
            return JsonResponse(
                {"message": "The data is incorrect", "status": "error"}
            )
    else:
        form = ManufacturerForm(instance=profile)
        
        formset_banners = ManufacturerBannerFormSet(
            prefix='manufacturer_banners',
            instance=profile,
        )
        
        formset_links = ManufacturerLinkFormSet(
            prefix='manufacturer_links',
            instance=profile,
        )

        return render(
            request,
            'manufacturer/manufacturer_profile_info.html',
            {
                'form': form,
                'manufacturer_banner_formset': formset_banners,
                'manufacturer_links_formset': formset_links,
            }
        )

def create_mailing(request):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    else:
        profile = Manufacturer.objects.filter(user=request.user).first()
        if request.method == 'POST':
            form = ManufacturerMailForm(request.POST, instance=profile)
            if form.is_valid():
                instance = form.save(commit=False)
                if profile:
                    instance.manufacturer = profile
                    profiles = Profile.objects.filter(accept_news=True, is_active=True)
                    instance.receiver_profile.add(*profiles)
                instance.save()
                instance.save_m2m()
                return JsonResponse(
                    {"message": "The manufacturer mail was created", "status": "success"}
                )
            else:
                return JsonResponse(
                    {"message": "The data is incorrect", "status": "error"}
                )


def update_manufacturer(request):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})

    profile = get_object_or_404(Profile, user=request.user)
    manufacturer = get_object_or_404(Manufacturer, profile=profile)
    if request.method == 'POST':
        form = ManufacturerUpdateForm(request.POST, instance=manufacturer)
        if form.is_valid():
            data = form.cleaned_data
            manufacturer = form.save(commit=False)
            manufacturer.name = data.get('name')
            manufacturer.phone = data.get('phone')
            manufacturer.email = data.get('email')
            manufacturer.save()
            return redirect('profile:profile_detail')
        else:
            return JsonResponse(
                {"message": "The data is incorrect", "status": "error"}
            )
    return JsonResponse({"redirect": reverse("profile:panel")})


class ListModelStatistic(LoginRequiredMixin, ListView):
    model = Manufacturer
    paginate_by = 10

    @staticmethod
    def model_exists(model_name):
        if model_name not in filter_data:
            return JsonResponse(
                {
                    "message": "Model not in accept list",
                    "status": "error",
                }
            )
        return True

    def get_template_names(self):
        model_name = self.request.GET.get('model', None)
        if self.model_exists(model_name):
            return [f"chart/{model_name}.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.request.GET.get('model__name', None)
        manufacturer = get_object_or_404(Manufacturer, profile__user=self.request.user)
        if not manufacturer.manufacturer_tariffs.filter(end_date__gte=date.today()).exists():
            return context

        if self.model_exists(model_name):
            if model_name != 'banner':
                context[f'list_{model_name}s'] = (filter_data[model_name]["model"].
                                                  filter(
                    **{f'{filter_data[model_name]["filter_args"]}': manufacturer}))
            else:
                banner_obj = filter_data["banner"]
                for obj in banner_obj:
                    context[f'manufacturer_{obj if obj != "manufacturer" else ""}_banners']\
                        = (banner_obj[obj]["model"].objects.filter(
                            **{f'{banner_obj[obj]["filter_args"]}': manufacturer}))

            return context


def get_statistic_data(request, model_name, pk, banner=False):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})

    if model_name not in filter_data:
        return JsonResponse(
            {
                "message": "Model not in accept list",
                "status": "error",
            }
        )
    if not filter_data[model_name]['model'].objects.filter(
            **{f'{filter_data[model_name]["filter_args"]}__profile__user': request.user},
            pk=pk).exists():
        return JsonResponse(
            {
                "message": "Current manufacturer user is not instance this objects pk",
                "status": "error",
            }
        )
    # data banner
    if banner:
        model_name = model_name + 'banner'
        return JsonResponse(
            {
                'data': {
                    'views': get_statistic_model_data(ViewAction, model_name, pk),
                }
            }
        )
    return JsonResponse(
            {
               'data': {
                   'likes': get_likes_statistic_data(model_name, pk),
                   'favorites': get_favorites_statistic_data(model_name, pk),
                   'views': get_statistic_model_data(ViewAction, model_name, pk),
                   'links_views': get_statistic_links_data(model_name, pk)
                   if model_name in ['brand', 'product'] else [],
                   'reviews': get_reviews_statistic_data(Review, 'product', pk)
                   if model_name == 'product' else [],
                   'comments': get_reviews_statistic_data(ArticleComment, 'article', pk)
                   if model_name == 'article' else [],
                   'conversion': get_statistic_model_data(Conversion, model_name, pk)
               }
            }
        )


class ListDraftArticles(LoginRequiredMixin, ListView):
    template_name = 'manufacturer/manufacturer_drafts.html'
    context_object_name = 'draft_articles'
    paginate_by = 4

    def get_queryset(self):
        manufacturer = get_object_or_404(Manufacturer, profile__user=self.request.user)
        return manufacturer.manufacturer_articles.filter(is_draft=True, is_active=True)


class ListPublishArticles(LoginRequiredMixin, ListView):
    template_name = 'manufacturer/manufacturer_publish.html'
    context_object_name = 'publish_articles'
    paginate_by = 4
    
    def get_queryset(self):
        manufacturer = get_object_or_404(Manufacturer, profile__user=self.request.user)
        return manufacturer.manufacturer_articles.filter(is_publish=True, is_active=True, is_draft=False)

class ListQuestionManufacturer(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'manufacturer/manufacturer_questions.html'
    context_object_name = 'manufacturer_questions'

    def get_queryset(self):
        return (Question.objects
                .filter(
                    product__brand__manufacturer__profile__user=self.request.user,
                    product__brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today()
                )
                .select_related('profile', 'product')
                .prefetch_related('question_answers')
                .annotate(author_id=F('profile__profile_author__id'))
                .annotate(answer_text=F('question_answers__text'))
        )


class ManufacturerArticleListView(ListView):
    model = Article
    template_name = 'manufacturer/manufacturer_articles.html'
    context_object_name = 'manufacturer_articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(manufacturer__profile__user=self.request.user,
                                      manufacturer__manufacturer_tariffs__end_date__gte=date.today(),
                                      is_draft=False, is_publish=True).select_related('manufacturer')


class CreateManufacturerAnswerView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        self.object = None
        model_type_dict = {
            'question': ManufacturerQuestionAnswer,
            'review': AnswerReview
        }
        model_type = self.request.POST.get('model_name')
        if model_type not in model_type_dict:
            return JsonResponse({"message": "There is no such model",
                                 "status": "error"})
        text = self.request.POST.get('text')

        if model_type == 'question':
            answer = model_type_dict[model_type].objects.filter(manufacturer__profile__user=self.request.user,
                                                                question=self.request.POST.get('question'))
        else:
            answer = model_type_dict[model_type].objects.filter(manufacturer__profile__user=self.request.user,
                                                                review=self.request.POST.get('review'))
        if answer:
            answer.update(text=text)
            answer = answer.first()
            return JsonResponse({"message": "Answer was update success!",
                                 "data": {
                                     'new_answer': answer.text,
                                     'date': answer.updated_at,
                                 },
                                 "status": "success"})

        manufacturer = Manufacturer.objects.filter(profile__user=self.request.user).first()
        if not manufacturer:
            return JsonResponse({"message": "There is no such profile manufacturer",
                                 "status": "error"})
        if model_type == 'question':
            question = get_object_or_404(Question, pk=self.request.POST.get('question'))
            new_answer = model_type_dict[model_type].objects.create(manufacturer=manufacturer,
                                                                    question=question,
                                                                    text=text)
        else:
            review = get_object_or_404(Review, pk=self.request.POST.get('review'))
            new_answer = model_type_dict[model_type].objects.create(manufacturer=manufacturer,
                                                                    review=review,
                                                                    text=text)
        return JsonResponse({"message": "Answer was created success!",
                             "data": {
                                 'new_answer': new_answer.text,
                             },
                             "status": "success"})


class ListReviewsManufacturer(LoginRequiredMixin, ListView):
    template_name = 'manufacturer/manufacturer_reviews.html'
    context_object_name = 'manufacturer_reviews'
    paginate_by = 5

    def get_queryset(self):
        return (Review.objects
                    .select_related('product', 'profile')
                    .prefetch_related('images', 'review_answers')
                    .filter(
                        product__brand__manufacturer__profile__user=self.request.user,
                        product__brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today()
                    )
                    .annotate(rating_normalized=F('rating') / 5 * 100)
                    .annotate(rating_int=Cast('rating_normalized', IntegerField()))
                    .annotate(answer_text=F('review_answers__text'))
                    .annotate(author_id=F('profile__profile_author__id'))
                )


class ListCommentManufacturer(LoginRequiredMixin, ListView):
    paginate_by = 11
    template_name = 'manufacturer/manufacturer_comments.html'
    context_object_name = 'manufacturer_comments'

    def get_queryset(self):
        return (ArticleComment.objects
                    .select_related('article', 'author', 'author__profile')
                    .prefetch_related()
                    .filter(article__manufacturer__profile__user=self.request.user, parent=None)
                ).order_by('-pk')


# Mailings
class CreateMailing(LoginRequiredMixin, ManufacturerStatus, View):
    def get_formset(self):
        PhoneFormSet = formset_factory(MailingPhoneFormSet, extra=1)
        EmailFormSet = formset_factory(MailingEmailFormSet, extra=1)
        return PhoneFormSet, EmailFormSet
        
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"redirect": reverse("profile:panel")})

        form = ManufacturerMailForm()
        PhoneFormSet, EmailFormSet = self.get_formset()
        
        email_formset = EmailFormSet(prefix='email__form')
        phone_formset = PhoneFormSet(prefix='phone__form')
        
        return render(request, 'mailing/mailing-create.html', {
            'form': form,
            'phone_formset': phone_formset,
            'email_formset': email_formset,
        })

    def post(self, request, *args, **kwargs):
        manufacturer = get_object_or_404(Manufacturer, profile__user=request.user)
        self.check_manufacturer_status(manufacturer)
        
        profile = Manufacturer.objects.filter(profile__user=request.user).first()
        # Check Forms
        PhoneFormSet, EmailFormSet = self.get_formset()
        form = ManufacturerMailForm(request.POST, request.FILES, instance=profile)
        email_formset = EmailFormSet(request.POST, prefix='email__form')
        phone_formset = PhoneFormSet(request.POST, prefix='phone__form')
        images = request.FILES
        if form.is_valid() and email_formset.is_valid() and phone_formset.is_valid():
            emails = []
            phones = []

            for form in email_formset:
                if form.is_valid():
                    emails.append(form.cleaned_data.get('email'))

            for form in phone_formset:
                if form.is_valid():
                    phones.append(form.cleaned_data.get('phone'))

            profiles = Profile.objects.filter(
                Q(phone__in=phones)
                |
                Q(email__in=emails)
            )

            # Save Form
            mailing = ManufacturerMailing()
            mailing.manufacturer = manufacturer
            mailing.company_name = request.POST.get('company_name', '')
            mailing.email = manufacturer.profile.email
            mailing.phone = manufacturer.profile.phone
            mailing.text = request.POST.get('text', '')
            mailing.save()

            # Add Profiles
            mailing.receiver_profile.set(profiles)

            # Add Banner
            banner = images.get('banner', None)
            if banner:
                mailing.banner = banner
                mailing.link_banner = request.POST.get('link_banner', None)

            # Add Background
            background_image = images.get('background_image', None)
            if background_image:
                mailing.background_image = background_image

            # Add Image
            main_image = images.get('image', None)
            if main_image:
                mailing.image = main_image

            mailing.save()
            return redirect('profile:profile_detail')
        else:
            return JsonResponse({'status': 'error', 'message': 'The data is incorrect'})

