from django.urls import path

from apps.services import views

app_name = "services"
urlpatterns = [
    path("create-tariff/", views.create_tariff, name='create_tariff'),
    path("change-tariff/<int:pk>/", views.change_tariff, name="change_tariff"),
    path("create-tariff-plan/", views.create_tariff_plan, name='create_tariff_plan'),
]
