from datetime import date
from django.db.models import Count, When, Case, Q
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseNotFound
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView
from pytils.translit import slugify

from apps.landing.models import MainBanner
from apps.blog.models import Article, ArticleComment, ArticleCommentPhoto, Complaint
from apps.blog.forms import ArticleComplaintForm, ArticleCommentForm
from apps.blog.forms import ArticleForm, ArticlePublish, CommentForm
from apps.manufacturers.models import Manufacturer
from apps.products.mixins import ViewMixin
from apps.profile.models import Author, AuthorHistory


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/list_articles.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        sorting_by = [
            {'value': 'created_at', 'text': 'Сначала новые'},
            {'value': '-created_at', 'text': 'Сначала старые'},
            {'value': 'title', 'text': 'По названию (А-Я)'},
            {'value': '-title', 'text': 'По названию (Я-А)'}
        ]

        sort_by = self.request.GET.get('sort_by', 'created_at')
        tags = self.request.GET.getlist('tag')

        q_objects = Q()

        if tags: q_objects &= Q(tag__slug__in=tags)
        if sort_by not in [el['value'] for el in sorting_by]:
            sort_by = 'created_at'

        self.object_list = (Article.objects
        .filter(
            Q(manufacturer__manufacturer_tariffs__end_date__gte=date.today()) &
            Q(is_publish=True) &
            Q(is_draft=False) &
            Q(is_active=True) &
            q_objects
        )
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
        context['tags'] = (Article.objects
                           .all()
                           .annotate(
            tag_is_null=Q(tag__isnull=False)
        )
                           .filter(tag_is_null=True)
                           .order_by('tag__slug')
                           .distinct('tag__slug')
                           .values('tag__name', 'tag__slug')
                           )
        context['discussions'] = ((ArticleComment.objects
                                    .select_related('article', 'article__manufacturer')
                                    .filter(
                                        is_publish=True,
                                        article__manufacturer__manufacturer_tariffs__end_date__gte=date.today(),
                                        article__is_publish=True,
                                        article__is_draft=False,
                                        article__is_active=True,
                                    )
                                    .order_by('article__title', 'created_at')
                                    ).values('article__title', 'article__slug')
                                  ).distinct('article__title')[:10]

        context['sortings_by'] = sorting_by
        return self.render_to_response(context)


class ArticleDetailView(DetailView, ViewMixin):
    model = Article
    template_name = 'blog/current_article.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        article = get_object_or_404(
            Article.objects
            .select_related('manufacturer', 'brand')
            .prefetch_related(
                'photos',
                'comments',
                'comments__photos',
                'comments__parent',
                'comments__author__profile__user',
                'brand__brand_products',
                'manufacturer__manufacturer_banners'
            )
            .annotate(
                likes_count=Count(Case(When(like_action__type_action=1, then=1))),
                views_count=Count(Case(When(views__type_action=1, then=1))),
                favorite_count=Count(Case(When(favorite_action__type_action=1, then=1))),
            )
            .order_by('comments'),
            manufacturer__manufacturer_tariffs__end_date__gte=date.today(),
            slug=self.kwargs.get(self.slug_url_kwarg),
            is_active=True
        )
        if article.manufacturer.profile.user != self.request.user and article.is_draft:
            raise Http404()
        return article

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_view_user(request, self.object)
        context = self.get_context_data(object=self.object)

        # Banners
        context['selection_banners'] = MainBanner.objects.filter(banner_selection=True)

        context['complaint_form'] = ArticleComplaintForm()
        return self.render_to_response(context)


def publish_draft_article(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    article = get_object_or_404(Article, pk=pk)
    if article.is_draft is False and article.is_publish:
        return JsonResponse({"message": "Article already publish", "status": "success"})
    article.is_draft = False
    article.is_publish = True
    article.save(update_fields=['is_draft', 'is_publish', ])
    return JsonResponse({"redirect": reverse("blog:articles")})


def delete_article(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    article = Article.objects.filter(pk=pk, manufacturer__profile__user=request.user).first()
    if not article:
        return JsonResponse(
            {
                "message": "Such article not exists!",
                "status": "error"
            }
        )
    if not article.is_active:
        return JsonResponse(
            {
                "message": "Article already deleted!",
                "status": "error"
            }
        )
    article.is_active = False
    article.save(update_fields=['is_active'])

    return JsonResponse(
        {
            "message": "Article success delete",
            "status": "complete"
        }
    )


def create_article(request):
    manufacturer = get_object_or_404(Manufacturer, profile__user=request.user)
    if request.method == "POST":
        history_manufacturer_last = manufacturer.manufacturer_tariffs.last()
        if not history_manufacturer_last:
            return JsonResponse(
                {
                    "message": "Manufacturer profile has not active tariff!",
                    "status": "error"
                }
            )

        if history_manufacturer_last.end_date < date.today():
            return JsonResponse(
                {
                    "message": "The current tariff has expired!",
                    "status": "error"
                }
            )
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.manufacturer = manufacturer
            article.slug = slugify(article.title)
            article.save()
            form.save_m2m()
        else:
            return JsonResponse(
                {"message": "The data is incorrect", "status": "error"}
            )
        if article.is_publish:
            return article.get_absolute_url()
        else:
            return redirect("manufacturer:manufacturer_drafts")
    else:
        context = {
            "form": ArticleForm(),
        }
        return render(request, "blog/create_article.html", context)


def publish_article(request, slug):
    article = Article.objects.filter(manufacturer__profile__user=request.user, slug=slug).last()
    if request.method == "POST":
        if not article:
            return JsonResponse(
                {
                    "message": "Current article not found!",
                    "status": "error"
                }
            )
        form = ArticlePublish(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.is_draft = True if request.POST.get('is_draft') == 'true' else False
            article.is_publish = True if request.POST.get('is_publish') == 'true' else False
            article.save()
            return JsonResponse(
                {"message": "Article Update Success", "status": "complete"}
            )
        else:
            return JsonResponse(
                {"message": "The data is incorrect", "status": "error"}
            )
    else:
        return redirect('manufacturer:drafts')


def update_article(request, slug):
    article = Article.objects.filter(manufacturer__profile__user=request.user, slug=slug).last()
    if request.method == "POST":
        if not article:
            return JsonResponse(
                {
                    "message": "Current article not found!",
                    "status": "error"
                }
            )
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            form.save_m2m()
        else:
            return JsonResponse(
                {"message": "The data is incorrect", "status": "error"}
            )
        if article.is_publish:
            return article.get_absolute_url()
        else:
            return redirect("manufacturer:manufacturer_drafts")

    else:
        context = {
            "form": ArticleForm(instance=article),
        }
        return render(request, "blog/update_article.html", context)


def create_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    author = get_object_or_404(Author, profile__user=request.user)
    last_history_obj = author.history.last()

    if not last_history_obj:
        return JsonResponse(
            {
                "message": f"History status of author not exists!",
                "status": "error"
            }
        )
    if last_history_obj.current_status != AuthorHistory.AuthorStatus.ACTIVE:
        return JsonResponse(
            {
                "message": f"Current author has block status",
                "status": "error"
            }
        )
    if request.method == 'POST':
        form = ArticleCommentForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            article = form.cleaned_data['article_id']
            article = Article.objects.filter(pk=article).first()
            parent = form.cleaned_data.get('parent', None)
            text = form.cleaned_data['text']

            # Проверка есть ли такой комментарий
            comment = form.check_exist(request.user)
            if comment:
                comment.text = text
                comment.save()
            else:
                if parent:
                    parent = ArticleComment.objects.filter(pk=parent).first()
                comment = form.save(commit=False)
                comment.text = text
                # comment.profile = author.profile
                comment.author = author
                comment.parent = parent
                comment.article = article
                comment.save()

            # Save Images
            for image in images:
                ArticleCommentPhoto.objects.create(comment=comment, photo=image)

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
        form = ArticleCommentForm()
        return render(request, 'add_comment.html', {'form': form})


def create_complaint(request):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    author = get_object_or_404(Author, profile__user=request.user)
    last_history_obj = author.history.last()

    if not last_history_obj:
        return JsonResponse(
            {
                "message": f"History status of author not exists!",
                "status": "error"
            }
        )
    if last_history_obj.current_status != AuthorHistory.AuthorStatus.ACTIVE:
        return JsonResponse(
            {
                "message": f"Current author has block status",
                "status": "error"
            }
        )
    if request.method == 'POST':
        form = ArticleComplaintForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data.get('title')
            text = data.get('text')
            object_id = data.get('object_id')
            object_type = data.get('object_type')

            title = dict(form.fields['title'].choices)[title]
            model = dict(form.fields['object_type'].choices)[object_type]
            # Создание Жалобы
            content_type = ContentType.objects.get_for_model(model)

            Complaint.objects.create(
                title=title,
                text=text,
                profile=author.profile,
                content_type=content_type,
                object_id=object_id,
            )
            return JsonResponse(
                {
                    'message': 'New complaint saved success!',
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


def get_new_comments_count(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comments = request.POST.getlist('objects_id[]', [])
            object_type = form.cleaned_data.get('object_type')
            model = dict(form.fields['object_type'].choices)[object_type]
            if object_type == '1':
                comments = (model.objects
                            .select_related('article')
                            .filter(
                                article__pk=pk,
                                parent=None,
                                is_publish=True,
                            )
                            .exclude(pk__in=comments)
                            )
            elif object_type == '2':
                comments = (model.objects
                            .select_related('overview')
                            .filter(
                                overview__pk=pk,
                                parent=None,
                                is_publish=True,
                            )
                            .exclude(pk__in=comments)
                            )
            elif object_type == '3':
                comments = (model.objects
                            .select_related('post')
                            .filter(
                                post__pk=pk,
                                parent=None,
                                is_publish=True,
                            )
                            .exclude(pk__in=comments)
                            )
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid Data'})

            return JsonResponse({
                'status': 'success',
                'message': 'Success Get Count Comments',
                'data': comments.count(),
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'The data is incorrect'})
    else:
        return JsonResponse({"redirect": reverse("profile:panel")})


def get_new_comments(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comments = request.POST.getlist('objects_id[]', [])
            object_type = form.cleaned_data.get('object_type')
            model = dict(form.fields['object_type'].choices)[object_type]
            type_ = 'comment'
            if object_type == '1':
                comments = (model.objects
                            .select_related('article')
                            .prefetch_related('photos')
                            .filter(
                                article__pk=pk,
                                parent=None,
                                is_publish=True,
                            )
                            .exclude(pk__in=comments)
                            )
            elif object_type == '2':
                comments = (model.objects
                            .select_related('overview')
                            .filter(
                                overview__pk=pk,
                                parent=None,
                                is_publish=True,
                            )
                            .exclude(pk__in=comments)
                            )
            elif object_type == '3':
                comments = (model.objects
                            .select_related('post')
                            .prefetch_related('comment_conversation_images')
                            .filter(
                                post__pk=pk,
                                parent=None,
                                is_publish=True,
                            )
                            .exclude(pk__in=comments)
                            )
                type_ = 'conversation'
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid Data', 'type': type_})

            if comments:
                html = render_to_string(
                    'utils/tags_for_new_comment.html',
                    {'comment': comments.first()},
                )
                return HttpResponse(html)
            else:
                return HttpResponseNotFound()
        else:
            return JsonResponse({'status': 'error', 'message': 'The data is incorrect'})
    else:
        return redirect('profile:profile_detail')

