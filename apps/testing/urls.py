from django.urls import path
from apps.testing import views

app_name = "testing"
urlpatterns = [
    path("test/", views.answer_test, name="answer_test"),
    path("test/result/", views.TestResultView.as_view(), name='result_test'),
]
