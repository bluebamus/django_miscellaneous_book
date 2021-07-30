from django.urls import include, path
from .views_ex.tdd_with_python_views import home_page, home_page_post
from .views_ex.tdd_with_post_views import home_page

app_name = "testcase_skills"

urlpatterns = [
    path("home/", home_page, name="testcase_home"),
    path("homepost/", home_page_post, name="testcase_home_post"),
    path("homepostrender/", home_page, name="testcase_home_post_render"),
    #path("login/", views.LoginView.as_view(), name="login"),
    #path("logout/", views.LogoutView.as_view(), name="logout"),
]