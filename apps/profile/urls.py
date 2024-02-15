from django.urls import path
from apps.profile import views

app_name = "profile"
urlpatterns = [

    # profiles urls
    # TODO change search parametr
    path("profile/", views.ProfileDetail.as_view(), name="profile_detail"),
    path("change-profile/", views.profile_change, name="change_profile"),
    path("delete-profile/", views.delete_profile, name="delete_profile"),
    path("profile/drafts/", views.ListDraftOverviews.as_view(), name='author_drafts'),
    path("profile/publish/", views.ListPublishOverviews.as_view(), name='author_publish'),
    path('publish-overview/<slug:slug>/', views.publish_overview, name='publish_overview'),
    
     # Comments
     path("profile/comments/", views.ProfileListCommentsOverview.as_view(), name="profile_comments"),

    # profile feedback block
    path("profile/feedback/questions/", views.ProfileFeedbackQuestionsView.as_view(),
         name='profile_feedback_questions'),
    path("profile/feedback/reviews/", views.ProfileFeedbackReviewsView.as_view(),
         name='profile_feedback_reviews'),
    path("profile/feedback/comments/", views.ProfileFeedbackCommentsView.as_view(),
         name='profile_feedback_comments'),
    path("profile/feedback/overviews/", views.ProfileFeedbackOverviewsView.as_view(),
         name='profile_feedback_overviews'),

    # actions with brand/product/article
    path("set-action/<slug:slug>/", views.set_action, name="set_action"),
    path("create-question/<int:pk>/", views.create_question, name="create_question"),

    # get favorite objects of profile
    path("favorite/", views.ProfileFavorite.as_view(), name="favorite_list"),

    # block correspondence
    path("profile/chats/", views.ProfileListChats.as_view(), name="profile_chats"),
    path("profile/support/", views.ListTechAppealView.as_view(), name="profile_appeals"),
    path("profile/support/create/", views.create_appeal, name='create_appeal'),

    # overviews urls
    path("overviews/", views.OverviewsList.as_view(), name="list_overviews"),
    path("overviews/<slug:slug>/", views.OverviewDetail.as_view(), name="detail_overview"),
    path("create-overview/", views.CreateOverview.as_view(), name="create_overview"),
    path("update-overview/<slug:slug>/", views.UpdateOverview.as_view(), name="update_overview"),
    path("delete-overview/<int:pk>/", views.delete_overview, name="delete_overview"),
    path("create-overview-comment/", views.create_comment, name="create_overview_comment"),

    # filtering and sorting articles/overviews/products
    path("filter-articles/", views.filter_objects, name='filter_objects'),
    path("sort-articles-date/", views.sort_objects_date, name='sort_objects_date'),

    # author urls
    # TODO change "author" on nickname?
    path("author/<str:nickname>/", views.AuthorWorksView.as_view(), name="get_author_works"),
    path("author-action/<int:pk>/", views.author_action, name="author_action"),

    path("add-service/", views.subscribe_service, name="subscribe_service"),
    path("author-statistic/", views.StatisticProfilesView.as_view(), name='statistic'),
    path("author-profile/<int:pk>/", views.AuthorProfile.as_view(), name="author-profile"),
    
    path('authors/', views.search_by_nickname, name='search_author')
]
