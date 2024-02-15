from django.urls import path

from apps.landing.views import LandingPageView, get_main_page

app_name = "landing"
urlpatterns = [
    path('', get_main_page, name='main_page'),
    path('<slug:slug>/', LandingPageView.as_view(), name='landing_page'),
]
