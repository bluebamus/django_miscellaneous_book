from django.urls import path
from .views import index

app_name = "orm_skills"

urlpatterns = [
    path("", index),
]
