from django.urls import path

from apps.blog import views
from apps.blog.models import ArticleComment
from apps.blog.views import ArticleListView, ArticleDetailView
from apps.profile.views import LikeDislikeView
from apps.tools.database_operations import ADD, REMOVE

app_name = "blog"
urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('create-article/', views.create_article, name='create_article'),
    path('update-article/<slug:slug>/', views.update_article, name='update_article'),
    path('publish-article/<slug:slug>/', views.publish_article, name='publish_article'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('delete-aricle/<int:pk>/', views.delete_article, name='delete_article'),
    path('create-complaint/', views.create_complaint, name='create_complaint'),
    path("create-article-comment/", views.create_comment, name="create_article_comment"),
    path('article_comment_like/<int:pk>/like/', LikeDislikeView.as_view(model=ArticleComment,
                                                                        type_action=ADD),
         name='article_comment_like'),
    path('article_comment_dislike/<int:pk>/dislike/', LikeDislikeView.as_view(model=ArticleComment,
                                                                              type_action=REMOVE),
         name='article_comment_dislike'),
    path('new-comments-count/<int:pk>/', views.get_new_comments_count, name='get_new_comments_count'),
    path('new-comments/<int:pk>/', views.get_new_comments, name='get_new_comments')
]
