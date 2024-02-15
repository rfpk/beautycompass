from django.urls import path
from django.contrib.sitemaps.views import sitemap

from . import views

app_name = "main"
urlpatterns = [
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register, name="register"),
    path("activate/", views.activate_user, name="activate_register"),
]


