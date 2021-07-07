from django.urls import path
from . import views

app_name = "log_test"

urlpatterns = [
    path("home/", views.home, name="home"),
    
]
