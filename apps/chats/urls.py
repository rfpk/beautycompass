from django.urls import path
from apps.chats import views
from apps.chats.views import ListPostsConversation, DetailPostConversation, CreatePostView

app_name = "chats"
urlpatterns = [
    path("create-message/", views.send_message, name="create_message"),
    path("get-chat/<int:pk>/", views.get_chat, name="get_chat"),
    path("create-conversation-post/", CreatePostView.as_view(), name="create_conversation_post"),
    path("create-conversation-comment/", views.create_comment, name="create_conversation_comment"),
    path("conversation/", ListPostsConversation.as_view(), name="list_conversations"),
    path("conversation/<slug:slug>/", DetailPostConversation.as_view(), name="detail_conversation"),
    path("conversation/name", views.search_posts_by_title, name='search_conversations')
]

