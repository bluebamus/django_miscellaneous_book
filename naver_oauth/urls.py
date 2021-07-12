from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from .views import (
    SocialLoginCallbackView,
    )

app_name = "naver_oauth"

urlpatterns = [
    path('user/login/', TemplateView.as_view(template_name='naver_oauth/login_form.html')),    
    #path('user/login/social/naver/callback/', ''),
    path('user/login/social/<str:provider>/callback/', SocialLoginCallbackView.as_view()),
]