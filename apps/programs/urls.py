from django.urls import path
from apps.programs import views

app_name = "programs"
urlpatterns = [
    path("program-list", views.ProgramsSaved.as_view(), name="program_list"),
    path("program/<int:pk>/", views.ProgramDetailView.as_view(), name="program_detail"),
    path("program/create/", views.ProgrammCreateView.as_view(), name="program_create"),
]
