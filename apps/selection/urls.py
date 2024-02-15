from django.urls import path
from apps.selection import views

app_name = "selection"
urlpatterns = [
    path("selection/", views.answer_selection, name="answer_selection"),
]
