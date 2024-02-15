from datetime import date, datetime
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.db.models.functions import RowNumber, Cast
from django.views import View
from django.template.loader import render_to_string
from django.db.models import Q, Window, F, IntegerField, Count, When, Case
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from pytils.translit import slugify
from django.contrib.auth import update_session_auth_hash

from apps.blog.forms import ArticleComplaintForm
from apps.blog.models import Article, ArticleComment
from apps.chats.models import Chat, ConversationPost, Message
from apps.products.mixins import ViewMixin
from apps.products.models import Brand, Product, Review
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from apps.manufacturers.forms import ManufacturerUpdateForm
from apps.manufacturers.models import ManufacturerMailing, Manufacturer, ManufacturerServiceHistory, ManufacturerQuestionAnswer
from apps.profile.models import Profile, Author, Overview, FavoriteAction, LikeAction, Appeal, \
    SubscribeAction, \
    GratitudeAction, OverviewComment, Question, AuthorHistory, AppealImage, logger
from apps.landing.models import MainBanner
from apps.profile.forms import QuestionForm, ProfileForm, AppealForm, CreateUpdateOverviewForm, CreateCommentForm, OverviewPublish
from apps.profile.services.author_rating_statistics import calculate_author_rating_period
from apps.profile.tools import model_action, check_profile_permission
from apps.services.models import AdditionalService
from apps.settings.models import BlockComment
from apps.tools.database_operations import ADD, REMOVE
from django.utils.translation import gettext_lazy as _


def create_question(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    if request.method == 'POST':
        profile = Profile.objects.filter(user=request.user).first()
        product = get_object_or_404(Product, pk=pk)
        if not profile:
            return JsonResponse(
                {"message": _("There is no such profile"), "status": "error"}
            )
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.profile = profile
            question.product = product
            question.save()
            return JsonResponse({
                'redirect': reverse('products:product_questions', args=[question.product.slug])
            })

        else:
            return JsonResponse(
                {"message": _("The data is incorrect"), "status": "error"}
            )


def profile_change(request):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    profile_change = Profile.objects.filter(user=request.user).first()
    if not profile_change:
        return JsonResponse(
            {"message": _("There is no such profile"), "status": "error"}
        )
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_change)
        if form.is_valid():
            # Save Form
            form.save()
            # Update Password
            if request.POST.get('password', None):
                user = form.save_password(request.user)
                update_session_auth_hash(request, user)
            
            return JsonResponse(
                {
                    "message": "Profile data was changed",
                    "status": "success",
                },
            )
        else:
            return JsonResponse(
                {"message": _("The data is incorrect"), "status": "error"}
            )

    else:
        context = {
            "form_change": ProfileForm(instance=profile_change),
        }
        return render(request, "site/update_profile.html", context)


def delete_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    profile_delete = Profile.objects.filter(user=request.user).first()
    if not profile_delete:
        return JsonResponse(
            {"message": "There is no such profile", "status": "error"}
        )
    profile_delete.save(delete=True)
    return JsonResponse({"message": "The profile delete", "status": "complete"})


def create_appeal(request):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    if request.method == 'POST':
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            return JsonResponse(
                {"message": _("There is no such profile"), "status": "error"}
            )
        form = AppealForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            appeal = form.save(commit=False)
            appeal.profile = profile
            appeal.save()

            # Save Images
            for image in images:
                AppealImage.objects.create(appeal=appeal, image=image)

            return redirect('profile:profile_appeals')
        else:
            return JsonResponse(
                {"message": _("The data is incorrect"), "status": "error"}
            )
    else:
        form = AppealForm()
        return render(request, 'create_appeal.html', {'form': form})


class ProfileMails(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profile/profile_mails.html'
    context_object_name = 'mails'
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    paginate_by = 5

    def get_queryset(self):
        return ManufacturerMailing.objects.filter(receiver_profile=self.request.user)


def set_action(request, slug):
    model_map = {
        'brand': Brand,
        'product': Product,
        'article': Article,
        'overview': Overview,
        'conversation': ConversationPost
    }
    action_map = {
        'like': LikeAction,
        'favorite': FavoriteAction
    }

    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    profile_action = Profile.objects.filter(user=request.user).first()
    if not profile_action:
        return JsonResponse(
            {"message": "There is no such profile", "status": "error"}
        )
    request_model_name = dict(request.POST.items()).get('model')
    model_class = model_map.get(request_model_name)
    model_type_action = action_map.get(dict(request.POST.items()).get('action'))
    if not model_class:
        return JsonResponse(
            {
                "message": "Unknown model name",
                "status": "error",
            }
        )
    if not model_type_action:
        return JsonResponse(
            {
                "message": "Unknown action type",
                "status": "error",
            }
        )
    object_model = get_object_or_404(model_class, slug=slug)
    if check_profile_permission(object_model, profile_action):
        # create new action
        new_obj_action = model_action(model_type_action, request_model_name,  object_model, profile_action)
        return JsonResponse(
            {
                "message": f"Action was changed",
                "status": "success",
                "data": new_obj_action.type_action
            }
        )


class ProfileFavorite(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = 'favorite_list'
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    paginate_by = 10

    model_map = [
        'brand',
        'product',
        'article',
        'overview'
    ]

    def model_exists(self, model_name):
        if model_name not in self.model_map:
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
            return [model_name + '/favorite_list.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        model_name = self.request.GET.get('model', None)
        if self.model_exists(model_name):
            favorite_list = FavoriteAction.objects.filter(profile=profile,
                                                          content_type__model=model_name).order_by('object_id',
                                                                                                   '-created_at').\
                                                                                            distinct('object_id')
            # TODO add filtering by type_action field
            context["favorite_list"] = [i for i in favorite_list if i.type_action == ADD]
            return context


class AuthorProfile(DetailView):
    model = Author
    template_name = 'profile/author_profile.html'
    context_object_name = 'profile'
    
    def get_object(self, queryset=None):
        author = get_object_or_404(
            Author.objects
                .select_related(
                    'profile',
                    'profile__user',
                    'profile__hair_type',
                    'profile__skin_type',
                    'profile__country',
                )
                .prefetch_related(
                    'history',
                    'overviews',
                    'profile__profile_reviews',
                    'profile__profile_reviews__images' ,
                    'profile__profile_reviews__product',
                    'profile__profile_conversation_posts',
                )
                .annotate(
                    current_status=F('history__current_status'),
                    close_at=F('history__close_at'),
                ),
                pk=self.kwargs.get('pk')
        )
        return author

    def get_pagination(self, type: str, query_param: str, paginate_by: int = 3):
        if type == 'overview':
            data = self.object.overviews.filter(
                is_publish=True,
                is_active=True,
                is_draft=False
            )
        elif type == 'review':
            data = self.object.profile.profile_reviews.all()

        paginator = Paginator(data, paginate_by)
        page = self.request.GET.get(query_param)
        page = page if page else 1

        try:
            data = paginator.page(page)
        except (InvalidPage, EmptyPage):
            data = paginator.page(paginator.num_pages)
        
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_type = self.object.type
        if profile_type == 'A':
            context['overviews'] = self.get_pagination('overview', 'page_overview', 4)

        profile_statistics = calculate_author_rating_period(self.object, 'total')
        context = context | profile_statistics
        context['profile_type'] = profile_type
        
        if context['profile'].profile.date_of_birth:
            self.object.profile.age = datetime.now().year - context['profile'].profile.date_of_birth.year

        context['reviews'] = self.get_pagination('review', 'page_review', 3)
        return context


class AuthorWorksView(LoginRequiredMixin, DetailView):

    def get(self, request, *args, **kwargs):
        author_types_lists = ['overviews', 'reviews', 'conversations']
        author = get_object_or_404(Author, profile__nickname=request.get(kwargs['nickname']))
        type_list = request.GET.get('lists', None)
        if type_list not in author_types_lists:
            return JsonResponse(
                {
                    "message": "Unknown type list!",
                    "status": "error",
                }
            )
        if type_list == 'overviews':
            data = author.overviews.filter(is_publish=True, is_draft=False).values()
        elif type_list == 'reviews':
            data = author.profile.profile_reviews.filter(
                is_publish=True,
                product__brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today()
            )
        else:
            data = author.profile.profile_conversation_posts.values()
        return JsonResponse(
            {
                "data": data,
            }
        )


class OverviewsList(ListView):
    model = Overview
    template_name = 'authors/list_overview.html'
    context_object_name = 'overviews'
    paginate_by = 8
    
    def get(self, request, *args, **kwargs):
        sorting_by = [
            { 'value': 'created_at', 'text': 'Сначала новые' },
            { 'value': '-created_at', 'text': 'Сначала старые' },
            { 'value': 'title', 'text': 'По названию (А-Я)' },
            { 'value': '-title', 'text': 'По названию (Я-А)' }
        ]
        
        sort_by = self.request.GET.get('sort_by', 'created_at')
        tags = self.request.GET.getlist('tag')
        
        q_objects = Q()
        
        if tags: q_objects &= Q(tag__slug__in=tags)
        if sort_by not in [el['value'] for el in sorting_by]:
            sort_by = 'created_at'
        
        self.object_list = (Overview.objects
                                .filter(
                                    Q(is_publish=True) &
                                    Q(is_draft=False) &
                                    Q(is_active=True) &
                                    q_objects
                                )
                                .select_related('author__profile')
                                .prefetch_related('comments')
                                .annotate(Count('comments', distinct=True))
                                .annotate(
                                    likes_count=Count(Case(When(like_action__type_action=1, then=1))),
                                    views_count=Count(Case(When(views__type_action=1, then=1))),
                                    favorite_count=Count(Case(When(favorite_action__type_action=1, then=1))),
                                )
                            ).order_by(sort_by)
        
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
        # Tags
        context['tags'] = (Overview.objects
                            .all()
                            .annotate(
                                tag_is_null=Q(tag__isnull=False)
                            )
                            .filter(tag_is_null=True)
                            .order_by('tag__slug')
                            .distinct('tag__slug')
                            .values('tag__name', 'tag__slug')
                        )
        # Sorting
        context['sortings_by'] = sorting_by

        # Discussions
        context['discussions'] = ((OverviewComment.objects
                                    .filter(
                                        is_publish=True,
                                        overview__is_publish=True,
                                        overview__is_draft=False,
                                        overview__is_active=True,
                                    )
                                    .order_by('overview__title', 'created_at')
                                  ).values('overview__title', 'overview__slug')
                                  ).distinct('overview__title')

        # Banners
        context['selection_banners'] = MainBanner.objects.filter(banner_selection=True)
        return self.render_to_response(context)
        


class OverviewDetail(DetailView, ViewMixin):
    model = Overview
    template_name = 'authors/detail_overview.html'
    context_object_name = 'overview'
    
    def get_object(self, queryset=None):
        overview = get_object_or_404(
            Overview.objects
            .select_related('brand')
            .prefetch_related('photos_overview', 'comments__author__profile__user', 'brand__brand_products')
            .annotate(
                likes_count=Count(Case(When(like_action__type_action=1, then=1))),
                views_count=Count(Case(When(views__type_action=1, then=1))),
                favorite_count=Count(Case(When(favorite_action__type_action=1, then=1))),
            )
            .order_by('comments'),
            slug=self.kwargs.get(self.slug_url_kwarg),
            is_active=True
        )
        if (overview.author.profile.user != self.request.user) and overview.is_draft:
            raise Http404()
        return overview

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_view_user(request, self.object)
        context = self.get_context_data(object=self.object)
        
        # Banners
        context['selection_banners'] = MainBanner.objects.filter(banner_selection=True)
        
        context['complaint_form'] = ArticleComplaintForm()
        return self.render_to_response(context)


class CreateOverview(LoginRequiredMixin, CreateView):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        context = {'form': CreateUpdateOverviewForm()}
        return render(request, 'overview/overview_form.html', context)

    def post(self, request, *args, **kwargs):
        author = get_object_or_404(Author, profile__user=request.user)
        history_last = author.history.last()
        if not history_last:
            return JsonResponse(
                {
                    "message": "Author has not status",
                    "status": "error",
                }
            )
        if history_last.current_status == AuthorHistory.AuthorStatus.ACTIVE:
            form = CreateUpdateOverviewForm(request.POST, request.FILES)
            if form.is_valid():
                overview = form.save(commit=False)
                overview.author = author
                overview.slug = slugify(overview.title)
                overview.save()
                author.rating += 1
                author.save(update_fields=['rating'], )
                form.save_m2m()
                return JsonResponse({"redirect": reverse("profile:list_overviews")})
            return JsonResponse(
                {"message": "The data is incorrect", "status": "error"}
            )
        else:
            return JsonResponse(
                {"message": 'Author has a block status', "status": "error"}
            )


class UpdateOverview(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    model = Overview

    def get(self, request, *args, **kwargs):
        context = {'form': CreateUpdateOverviewForm(instance=self.get_object())}
        return render(request, 'overview/overview_form.html', context)

    def post(self, request, *args, **kwargs):
        author = get_object_or_404(Author, profile__user=request.user)
        history_last = author.history.last()
        if not history_last:
            return JsonResponse(
                {
                    "message": f"History status of author not exists!",
                    "status": "error"
                }
            )
        if history_last.current_status != AuthorHistory.AuthorStatus.ACTIVE:
            return JsonResponse(
                {
                    "message": f"Author has a block status",
                    "status": "error"
                }
            )
        else:
            form = CreateUpdateOverviewForm(request.POST, request.FILES, instance=self.get_object())
            if form.is_valid():
                overview = form.save(commit=False)
                overview.save()
                form.save_m2m()
                return JsonResponse({"redirect": reverse("profile:list_overviews")})
            return JsonResponse(
                {"message": "The data is incorrect", "status": "error"}
            )


def publish_overview(request, slug):
    overview = Overview.objects.filter(
        author__profile__user=request.user,
        slug=slug,
    ).last()
    if request.method == 'POST':
        if not overview:
            return JsonResponse(
                {
                    "message": "Current overview not found!",
                    "status": "error"
                }
            )
        form = OverviewPublish(request.POST, instance=overview)
        if form.is_valid():
            overview = form.save(commit=False)
            overview.is_draft =  True if request.POST.get('is_draft') == 'true' else False
            overview.is_publish = True if request.POST.get('is_publish') == 'true' else False
            overview.save()
            return JsonResponse(
                {"message": "Overview Update Success", "status": "complete"}
            )
        else:
            return JsonResponse(
                {"message": "The data is incorrect", "status": "error"}
            )
    else:
        return redirect('profile:author_drafts')

def filter_objects(request):
    model_types = {
        'article': Article,
        'overview': Overview
    }
    request_model = request.GET.getlist('model')
    if request_model not in model_types:
        return JsonResponse(
            {
                'message': 'Current model unknown!',
                'status': 'error'
            }
        )
    tag = request.GET.getlist('tags')
    if model_types == 'article':
        filtering_obj = (model_types['request_model'].objects.
                         filter(Q(manufacturer__manufacturer_tariffs__end_date__gte=date.today()) &
                                Q(tag__in=tag)).values())
    else:
        filtering_obj = model_types['request_model'].objects.filter(Q(tag__in=tag)).values()
    return JsonResponse({'data': filtering_obj})


def sort_objects_date(request):
    sorting_types = {
        'sorting_types_blog': ['newest', 'old', 'popular'],
        'sorting_types_product': ['newest', 'old', 'name-max', 'name-min']
    }
    model_types = {
        'article': Article,
        'overview': Overview,
        'product': Product
    }
    filter_types = {
        'article': {'manufacturer__manufacturer_tariffs__end_date__gte': (date.today())},
        'product': {'series__brand__manufacturer__manufacturer_tariffs__end_date__gte': (date.today())}
    }
    request_type = request.GET.get('order', None)
    request_model = request.GET.get('model', None)

    if request_model not in model_types:
        return JsonResponse(
            {
                'message': 'Current model unknown!',
                'status': 'error'
            }
        )
    if request_model != 'product':
        if request_type not in sorting_types['sorting_types_blog']:
            return JsonResponse(
                {
                    'message': 'Current type unknown!',
                    'status': 'error'
                }
            )
        else:
            if request_type not in sorting_types['sorting_types_product']:
                return JsonResponse(
                    {
                        'message': 'Current type unknown!',
                        'status': 'error'
                    }
                )
    if request_model != 'overview':
        obj = model_types['request_model'].objects.filter(**filter_types[request_model])
    else:
        obj = model_types['request_model'].objects
    if request_type == 'newest':
        sort_objects = obj.order_by('-created_at').values()
    elif request_type == 'old':
        sort_objects = obj.order_by('created_at').values()
    elif request_type == 'popular':
        # TODO optimization
        list_obj = obj.all()
        for obj_item in list_obj:
            views = obj_item.views.count()
            likes = obj_item.get_like_count()
            add_favorite = obj_item.get_favorite_count()
            comments = obj_item.comments.cout()
            obj_item.total_rating = views + likes + add_favorite + comments
            obj_item.save()
        sort_objects = obj.order_by('-total_rating').values()

    elif request_type == 'name-max':
        sort_objects = obj.order_by('-name').values()
    else:
        sort_objects = obj.order_by('name').values()
    return JsonResponse({'data': sort_objects})


def author_action(request, pk):
    action_map = {
        'subscribe': SubscribeAction,
        'gratitude': GratitudeAction
    }
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    action_name = dict(request.POST.items()).get('model')
    if action_name not in action_map:
        return JsonResponse(
            {
                "message": 'Unknown action name!',
                "status": "error"
            }
        )
    author_action = get_object_or_404(Author, profile__user=request.user)
    author = get_object_or_404(Author, pk=pk)
    if author.type != "A":
        return JsonResponse(
            {
                "message": 'Can not to subscribe or gratitude on reader account!',
                "status": "error"
            }
        )
    if author_action == author:
        return JsonResponse(
            {
                "message": 'Can not to subscribe or gratitude on yourself account!',
                "status": "error"
            }
        )
    last_object_action = action_map[action_name].objects.filter(author=author,
                                                                author_action=author_action).last()
    if last_object_action and last_object_action.type_action == ADD:
        type_action = REMOVE
        author.rating -= 1
    else:
        type_action = ADD
        author.rating += 1
    author.save(update_fields=['rating'], )
    new_object_action = action_map[action_name].objects.create(author=author, author_action=author_action,
                                                               type_action=type_action)

    return JsonResponse(
        {
            "message": 'Action successfully set!',
            "new_status": new_object_action.type_action,
            "status": "success"
        }
    )


class LikeDislikeView(LoginRequiredMixin, View):
    model = None
    type_action = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        profile = get_object_or_404(Profile, user=request.user)
        action, status_create = LikeAction.objects.get_or_create(content_type=ContentType.objects.get_for_model(obj),
                                                                 object_id=obj.id, profile=profile,
                                                                 defaults={'type_action': self.type_action}
                                                                 )
        if not status_create:
            if action.type_action != self.type_action:
                action.type_action = self.type_action
            else:
                action.type_action = None
            action.save()
        return JsonResponse(
            {
                "new_action_like": obj.reaction.filter(type_action=ADD).count(),
                "new_action_dislike": obj.reaction.filter(type_action=REMOVE).count()
            }
        )


def search_by_nickname(request):
    nickname = request.GET.get('nickname')
    type_period = request.GET.get('period')
    type_ = request.GET.get('type', None)
    authors = Author.objects.select_related('profile').filter(profile__nickname__icontains=nickname)
    if type_:
        authors = authors.exclude(profile__user=request.user)
        html = render_to_string(
            'utils/tags_for_chat.html', {'data': authors[:4]}
        )
        return HttpResponse(html)
    else:
        if type_period == 'total':
            authors = (authors
                        .filter(type='A')
                        .order_by('-rating')
                        .annotate(
                            position=Window(expression=RowNumber(), order_by=F('rating').desc())
                        )
                    )
            html = render_to_string(
                'utils/tags_for_author.html', {'data': authors, 'type_period': type_period}
            )
            return HttpResponse(html)
        elif type_period == 'readers':
            authors = authors.filter(type='R')
        else:
            authors = authors.filter(type='A')

        list_rating_authors = [
            {'author': author, 'rating': author.get_rating_value(period=type_period)} for author in authors]

        authors = sorted(list_rating_authors, key=lambda d: d['rating'], reverse=True)

        for i, author in enumerate(authors):
                author['position'] = i + 1

        html = render_to_string(
            'utils/tags_for_author.html', {'data': authors, 'type_period': type_period}
        )
        return HttpResponse(html)


class StatisticProfilesView(ListView):
    model = Author
    template_name = 'profile/author_rating.html'
    paginate_by = 10

    def get_queryset(self):
        return Author.objects.select_related('profile')

    def get_paginate_data(self, context) -> None:
        paginator = Paginator(context['order_authors'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_authors = paginator.page(page)
        except PageNotAnInteger:
            page_authors = paginator.page(1)
        except EmptyPage:
            page_authors = paginator.page(paginator.num_pages)
        context['page_authors'] = page_authors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period = self.request.GET.get('period', 'total')
        context['types'] = {'total': 'За все время',
                            'year': 'За год',
                            'quarter': 'За три месяца',
                            'month': 'За месяц',
                            'week': 'За неделю',
                            'readers': 'Читатели'
                            }
        context['type_period'] = period

        authors = self.get_queryset()
        if period == 'total':
            context['order_authors'] = authors.filter(type='A').order_by('-rating').annotate(position=Window(
                expression=RowNumber(), order_by=F('rating').desc()))
            self.get_paginate_data(context)
            return context
        elif period == 'readers':
            authors = authors.filter(type='R')
        else:
            authors = authors.filter(type='A')
        list_rating_authors = [{'author': author, 'rating': author.get_rating_value(period=period)} for author in
                               authors]
        context['order_authors'] = sorted(list_rating_authors, key=lambda d: d['rating'], reverse=True)

        for i, author in enumerate(context['order_authors']):
            author['position'] = i + 1
        self.get_paginate_data(context)

        return context


def subscribe_service(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    additional_service = get_object_or_404(AdditionalService, pk=pk)
    manufacturer = get_object_or_404(Manufacturer, profile__user=request.user)
    ManufacturerServiceHistory.objects.create(service=additional_service,
                                              manufacturer=manufacturer)
    logger.info(f'Manufacturer({manufacturer.profile.email}) subscribe on AdditionalService({additional_service.pk}')


class ListTechAppealView(LoginRequiredMixin, ListView):
    model = Appeal
    template_name = 'profile/chat-tech.html'
    context_object_name = 'appeals'
    paginate_by = 9
    
    def get(self, request, *args, **kwargs):
        self.object_list = get_object_or_404(Profile, user=self.request.user).profile_appeals.all()
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
        context['form'] = AppealForm()
        return self.render_to_response(context)

class ListDraftOverviews(LoginRequiredMixin, ListView):
    template_name = 'authors/list_overviews_drafts.html'
    context_object_name = 'draft_overviews'
    paginate_by = 3    
    
    def get(self, request, *args, **kwargs):
        self.object_list = (Overview.objects
                                .filter(
                                    author__profile__user=self.request.user,
                                    is_draft=True,
                                    is_active=True
                                )
                                .select_related('author', 'brand', 'author__profile')
                                .prefetch_related('tag')
                            ).order_by('created_at')

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
        return self.render_to_response(context)


class ListPublishOverviews(LoginRequiredMixin, ListView):
    template_name = 'authors/list_overviews_publish.html'
    context_object_name = 'publish_overviews'
    paginate_by = 3

    def get_queryset(self):
        return (Overview.objects
                    .filter(
                        author__profile__user=self.request.user,
                        is_publish=True,
                        is_active=True,
                        is_draft=False,
                    )
                    .select_related('author', 'brand', 'author__profile')
                    .prefetch_related('tag')
                ).order_by('created_at')


def delete_overview(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    overview = Overview.objects.filter(pk=pk, author__profile__user=request.user).first()
    if not overview:
        return JsonResponse(
            {
                "message": "Such overview not exists!",
                "status": "error"
            }
        )
    if not overview.is_active:
        return JsonResponse(
            {
                "message": "Overview already deleted!",
                "status": "error"
            }
        )
    overview.is_active = False
    if overview.author.rating > 0:
        overview.author.rating -= 1
        overview.author.save(update_fields=['rating'], )
    overview.save(update_fields=['is_active'], )

    return JsonResponse(
        {
            "message": "Overview success delete",
            "status": "complete"
        }
    )


def create_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    author = get_object_or_404(Author, profile__user=request.user)
    last_history_obj = author.history.last()

    if last_history_obj.current_status != AuthorHistory.AuthorStatus.ACTIVE:
        return JsonResponse(
            {
                "message": f"Current author has block status",
                "status": "error"
            }
        )
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            overview = form.cleaned_data['overview']
            overview = Overview.objects.filter(pk=overview).first()
            parent = form.cleaned_data.get('parent', None)
            text = form.cleaned_data['text']

            comment = form.check_exist(request.user)
            if comment:
                comment.text = text
                comment.save()
            else:
                if parent:
                    parent = OverviewComment.objects.filter(pk=parent).first()
                comment = form.save(commit=False)
                comment.text = text
                comment.author = author
                comment.parent = parent
                comment.overview = overview
                comment.save()
            
            return JsonResponse(
                {
                    'message': 'New comment saved success!',
                    'status': 'success'
                }
            )
        else:
            return JsonResponse(
                {
                    'message': 'Form is a not valid',
                    'status': 'error'
                }
            )

    else:
        form = CreateCommentForm()
        return render(request, 'add_comment.html', {'form': form})


def block_profile_comment(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    profile = get_object_or_404(Profile, user=request.user)
    if not profile.is_admin():
        return JsonResponse(
            {"message": "Current user has not status admin for delete comments",
             "status": "error"}
        )
    overview_comment = get_object_or_404(OverviewComment, pk=pk)
    block_type = BlockComment.objects.filter(reasons=request.POST.get('block_type')).first()
    if not block_type:
        return JsonResponse(
            {"message": "No find such block type",
             "status": "error"}
        )
    overview_comment.block_type = block_type
    overview_comment.is_publish = False

    #update rating
    overview_comment.author.rating -= 1
    overview_comment.overview.author.rating -= 1
    overview_comment.author.save(update_fields=['rating'])
    overview_comment.overview.author.save(update_fields=['rating'])
    overview_comment.save()

    if OverviewComment.objects.filter(parent=overview_comment).exists():
        for child in overview_comment.answers.all():
            child.is_publish = False
            child.save(update_fields=['is_publish'])


class ProfileFeedbackQuestionsView(LoginRequiredMixin, ListView):
    template_name = 'profile/profile_questions.html'
    context_object_name = 'questions'
    paginate_by = 5
    
    def get(self, request, *args, **kwargs):
        self.object_list = (Question.objects
                    .filter(
                        profile__user=self.request.user,
                        product__brand__manufacturer__manufacturer_tariffs__end_date__gte=date.today()
                    )
                    .prefetch_related('question_answers')
                    .select_related('profile', 'product', 'product__series')
                    .annotate(
                        answer_manufacturer_name=F('question_answers__manufacturer__name'),
                        answer_manufacturer_logo=F('question_answers__manufacturer__logo'),
                        answer_manufacturer_id=F('question_answers__manufacturer__id'),
                    )
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
        return self.render_to_response(context)


class ProfileFeedbackReviewsView(LoginRequiredMixin, ListView):
    template_name = 'profile/feedback_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 5
    
    def get(self, request, *args, **kwargs):
        self.object_list = (Review.objects
                    .filter(
                        profile__user=self.request.user,
                        is_publish=True,
                    )
                    .select_related('product', 'profile', 'product__brand__manufacturer', 'product__series')
                    .prefetch_related('review_answers', 'images')
                    .annotate(
                        answer_text=F('review_answers__text'),
                        answer_date=F('review_answers__created_at'),
                        answer_manufacturer_logo=F('review_answers__manufacturer__logo'),
                        answer_manufacturer_name=F('review_answers__manufacturer__name'),
                        answer_manufacturer_id=F('review_answers__manufacturer__id'),
                    )
                    .annotate(review_rating_normalized=F('rating') / 5 * 100)
                    .annotate(review_rating_int=Cast('review_rating_normalized', IntegerField()))
                    .annotate(product_rating_normalized=F('product__rating') / 5 * 100)
                    .annotate(product_rating_int=Cast('product_rating_normalized', IntegerField()))
                    .annotate(
                        likes_count=Count(Case(When(reaction__type_action=1, then=1))),
                        dislikes_count=Count(Case(When(reaction__type_action=0, then=1)))
                    )
                    .order_by('-pk', '-review_answers__created_at')
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
        return self.render_to_response(context)


class ProfileFeedbackCommentsView(LoginRequiredMixin, ListView):
    template_name = 'profile/profile_feedback_comments.html'
    context_object_name = 'comments'
    paginate_by = 11
    
    def get(self, request, *args, **kwargs):
        self.object_list =  (ArticleComment.objects
                                .exclude(Q(article__manufacturer__profile__user=self.request.user))
                                .filter(
                                    article__manufacturer__manufacturer_tariffs__end_date__gte=date.today(),
                                    author__profile__user=self.request.user
                                )
                                .annotate(
                                    likes_count=Count(Case(When(reaction__type_action=1, then=1))),
                                )
                                .select_related('article', 'parent', 'author', 'author__profile')
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
        return self.render_to_response(context)


class ProfileFeedbackOverviewsView(LoginRequiredMixin, ListView):
    template_name = 'profile/profile_overviews.html'
    context_object_name = 'profile_overviews_comments'
    paginate_by = 10

    def get_queryset(self):
        return OverviewComment.objects.filter(author__profile__user=self.request.user).select_related('overview',
                                                                                                      'parent',
                                                                                                      'author')


class ProfileListChats(LoginRequiredMixin, ListView):
    template_name = 'profile/chat-persons.html'
    context_object_name = 'chats'
    paginate_by = 9
    
    def get(self, request, *args, **kwargs):
        self.object_list = (Chat.objects
                    .filter(participants__user=self.request.user)
                    .prefetch_related('chat_messages')
                    .annotate(
                        avatar=F('chat_messages__sender__avatar'),
                        first_name=F('chat_messages__sender__first_name'),
                        last_name=F('chat_messages__sender__last_name'),
                        last_message=F('chat_messages__text'),
                        date=F('chat_messages__date'),
                    )
                    .order_by('-pk', '-chat_messages__date')
                ).distinct('pk')
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
        return self.render_to_response(context)


# Personal Area
class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile
    
    def get_object(self, queryset=None):
        return get_object_or_404(Author, profile__user=self.request.user)
    
    def get_manufacturer(self):
        profile = self.object.profile
        return (Manufacturer.objects
                    .prefetch_related('manufacturer_brands')
                    .filter(profile=profile)
                    .first())
    
    def paginate(self, data, type: str, query_param: str, context: dict[str, Any], paginate_by: int = 5):
        if data:
            paginator = Paginator(data, paginate_by)
            page = self.request.GET.get(query_param)
            page = page if page else 1

            try:
                data = paginator.page(page)
            except (InvalidPage, EmptyPage):
                data = paginator.page(paginator.num_pages)
            
            context[type] = data
    
    def get_pagination(self, context: dict[str, Any]):
        brands = self.get_manufacturer().manufacturer_brands.all()
        self.paginate(brands, type='brands', query_param='brand_page', context=context)
        
        for brand in brands:
            self.paginate(brand.series.all(), type=f'series_{brand.id}', query_param='series_page', context=context)
            for series in brand.series.all():
                self.paginate(series.products.all(), type=f'products_{series.id}', query_param='products_page', context=context)
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        profile = self.object.profile
        
        if self.object.type == Author.AuthorType.MANUFACTURER:
            manufacturer = self.get_manufacturer()
            self.get_pagination(context)
            
            form = ManufacturerUpdateForm(instance=manufacturer)
            return render(
                request,
                'manufacturer/page-profile-info.html',
                {
                    'manufacturer': manufacturer,
                    'form': form,
                    **context
                }
            )
        else:
            form = ProfileForm(instance=profile)
            return render(
                request,
                'profile/personal_area.html',
                {
                    'profile': profile,
                    'form': form,
                }
            )


# Comments
class ProfileListCommentsOverview(LoginRequiredMixin, ListView):
    template_name = 'profile/comments.html'
    context_object_name = 'profile_comments'
    paginate_by = 11
    
    def get(self, request, *args, **kwargs):
        self.object_list = (OverviewComment.objects
                    .filter(overview__author__profile__user=self.request.user)
                    .exclude(author__profile__user=self.request.user)
                    .select_related('overview', 'parent', 'author', 'author__profile')
                    .annotate(
                        likes_count=Count(Case(When(reaction__type_action=1, then=1))),
                    )
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
        return self.render_to_response(context)
