from django.urls import path

from apps.manufacturers import views
from apps.manufacturers.models import AnswerReview
from apps.manufacturers.views import ManufacturerArticleListView, CreateMailing
from apps.profile.views import LikeDislikeView
from apps.tools.database_operations import ADD, REMOVE

app_name = "manufacturer"

urlpatterns = [
    # manufacturer drafts and publish articles
    path("manufacturer/create/", views.ManufacturerCreate.as_view(), name="manufacturer_create"),
    path("manufacturer/<int:pk>/", views.ManufacturerProfile.as_view(), name="profile_manufacturer"),

    path("manufacturer/drafts/", views.ListDraftArticles.as_view(), name='manufacturer_drafts'),
    path("manufacturer/publish/", views.ListPublishArticles.as_view(), name='manufacturer_publish'),
    path('manufacturer/articles/', ManufacturerArticleListView.as_view(), name='manufacturer_articles'),
    path('manufacturer/update/', views.update_manufacturer, name='manufacturer_update'),

    # block new
    path("manufacturer/questions/", views.ListQuestionManufacturer.as_view(), name='manufacturer_questions'),
    path("manufacturer/reviews/", views.ListReviewsManufacturer.as_view(), name='manufacturer_reviews'),
    path("manufacturer/comments/", views.ListCommentManufacturer.as_view(), name='manufacturer_comments'),

    # block statistics
    path("statistic/<str:model_name>/", views.ListModelStatistic.as_view(), name="manufacturer_statistic_model"),
    path("statistic/<str:model_name>/<int:pk>/", views.get_statistic_data, name='statistic_data_object'),

    # block correspondence
    # profile.urls.py file

    # ajax methods
    path("create-manufacturer-answer/", views.CreateManufacturerAnswerView.as_view(), name='manufacturer_create_answer'),
    path("manufacturer/info/", views.change_profile_manufacturer, name="change_manufacturer"),
    path('answer_review_like/<int:pk>/like/', LikeDislikeView.as_view(model=AnswerReview, type_action=ADD),
         name='answer_review_like'),
    path('answer_review_dislike/<int:pk>/dislike/', LikeDislikeView.as_view(model=AnswerReview,
                                                                            type_action=REMOVE),
         name='answer_review_dislike'),
    
    # Mailing
    path('create-mailing/', CreateMailing.as_view(), name='create-mailing'),
]
