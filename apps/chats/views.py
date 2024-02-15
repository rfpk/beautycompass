from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Count, Case, When, F

from apps.blog.forms import ArticleComplaintForm
from apps.landing.models import MainBanner
from apps.chats.forms import MessageForm, ConversationForm, CreateCommentForm
from apps.products.mixins import ViewMixin
from apps.profile.models import Profile, Author, AuthorHistory
from apps.chats.models import Chat, Message, ConversationPost, CommentConversation, ImageComment
from django.utils.translation import gettext_lazy as _


def send_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            chat = Chat.objects.filter(participants=form.cleaned_data['sender']).\
                                filter(participants=form.cleaned_data['receiver']).first()
            if chat:
                Message.objects.create(title=form.cleaned_data['title'],
                                       text=form.cleaned_data['text'],
                                       profile_sent=form.cleaned_data['sender'],
                                       profile_get=form.cleaned_data['receiver'],
                                       chat=chat)
            else:
                receiver = Profile.objects.filter(pk=request.POST.get('receiver')).first()
                sender = Profile.objects.filter(user=request.user).first()

                new_chat = Chat.objects.create(title=request.POST.get('title', ''))
                new_chat.participants.add(sender, receiver)

                # Save Message
                Message.objects.create(title=form.cleaned_data['title'],
                                       text=form.cleaned_data['text'],
                                       sender=sender,
                                       receiver=receiver,
                                       chat=new_chat)
            return redirect(reverse("profile:profile_chats"))
        else:
            return JsonResponse(
                {"message": _("The data is incorrect"), "status": "error"}
            )
    else:
        form = MessageForm()
        return render(request, "send_message.html", {'form': form})


def get_chat(request, pk=None):
    context = {}
    if pk:
        chat = get_object_or_404(
            Chat.objects.prefetch_related('chat_messages', 'participants'),
            pk=pk)
        context['curren_chat'] = chat
        return render(request, "chats/current_chat.html", context)
    else:
        profile = Profile.objects.filter(user=request.user).first()
        chats_list = Chat.objects.filter(participants=profile).first()
        context['chats_list'] = chats_list.profile_chats
        return render(request, "all_chats.html", context)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = ConversationPost
    form_class = ConversationForm
    template_name = 'chats/conversation_list.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            profile = get_object_or_404(Profile, user=self.request.user)
            post = form.save(commit=False)
            post.profile = profile
            post.slug = slugify(post.title)
            post.save()
            form.save_m2m()
            return redirect("chats:list_conversations")
        else:
            return self.form_invalid(form)


def create_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": reverse("profile:panel")})
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
                "message": f"Current author has block status",
                "status": "error"
            }
        )
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():
            post = form.cleaned_data['post']
            post = ConversationPost.objects.filter(pk=post).first()
            parent = form.cleaned_data.get('parent', None)
            text = form.cleaned_data['text']
            
            # Проверка есть ли такой комментарий
            comment = form.check_exist(request.user)
            if comment:
                comment.text=text
                comment.save()
            else:
                if parent:
                    parent = CommentConversation.objects.filter(pk=parent).first()
                comment = form.save(commit=False)
                comment.text = text
                comment.author = author
                comment.parent = parent
                comment.post = post
                comment.save()
            
            # Save Images
            for image in images:
                ImageComment.objects.create(comment=comment, image=image)
            
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


def search_posts_by_title(request):
    post_name = request.GET.get('post_name')
    
    conversations = (ConversationPost.objects
                        .filter(is_publish=True, title__icontains=post_name)
                        .select_related('profile')
                        .annotate(
                            likes_count=Count(Case(When(like_action__type_action=1, then=1))),
                            views_count=Count(Case(When(views__type_action=1, then=1))),
                            favorite_count=Count(Case(When(favorite_action__type_action=1, then=1))),
                        )
                        .annotate(author_id=F('profile__profile_author__id'))
                    )
    html = render_to_string(
        'utils/post_for_conversations.html', {'posts': conversations}
    )
    return HttpResponse(html)

class ListPostsConversation(ListView):
    model = ConversationPost
    template_name = 'chats/conversation_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get(self, request, *args, **kwargs):
        self.object_list = (ConversationPost.objects
                                .filter(is_publish=True)
                                .select_related('profile')
                                .annotate(
                                    likes_count=Count(Case(When(like_action__type_action=1, then=1))),
                                    views_count=Count(Case(When(views__type_action=1, then=1))),
                                    favorite_count=Count(Case(When(favorite_action__type_action=1, then=1))),
                                )
                                .annotate(author_id=F('profile__profile_author__id'))
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


class DetailPostConversation(DetailView, ViewMixin):
    model = ConversationPost
    template_name = 'chats/conversation_detail.html'
    context_object_name = 'post'
    
    def get_object(self, queryset=None):
        return get_object_or_404(ConversationPost.objects
                                    .select_related('profile')
                                    .prefetch_related(
                                        'post_conversation_images',
                                        'tag',
                                        'comments',
                                        'comments__parent',
                                        'comments__author__profile__user',
                                        'comments__comment_conversation_images'
                                    )
                                    .annotate(Count('comments', distinct=True))
                                    .annotate(
                                        likes_count=Count(Case(When(like_action__type_action=1, then=1))),
                                        views_count=Count(Case(When(views__type_action=1, then=1))),
                                        favorite_count=Count(Case(When(favorite_action__type_action=1, then=1))),
                                    )
                                    .annotate(author_id=F('profile__profile_author__id'))
                                    .order_by('comments'),
                                    is_publish=True, slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super(DetailPostConversation, self).get_context_data(**kwargs)
        
        # Banners
        context['selection_banners'] = MainBanner.objects.filter(banner_selection=True)
        
        context['complaint_form'] = ArticleComplaintForm()
        return context
