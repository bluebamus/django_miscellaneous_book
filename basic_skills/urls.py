from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from .views import FlavorListView

app_name = "basic_skills"

urlpatterns = [
    path('', FlavorListView.as_view()),
]
