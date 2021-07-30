from django.urls import path
from .views_ex.tdd_with_python_views import home_page

app_name = "testcase_skills"

urlpatterns = [
    path("home/", home_page, name="home"),
    #path("login/", views.LoginView.as_view(), name="login"),
    #path("logout/", views.LogoutView.as_view(), name="logout"),
]
