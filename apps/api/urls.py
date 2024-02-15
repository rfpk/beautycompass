from django.urls import path, include
from rest_framework import routers

from apps.api import views


app_name = "api"
router = routers.SimpleRouter()
router.register(r'manufacturer-articles', views.ManufacturerArticlesView, basename='ManufacturerArticles')


urlpatterns = [
    path('api/', include(router.urls)),
]
