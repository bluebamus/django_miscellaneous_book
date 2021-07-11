from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    hello, 
    list_article, 
    detail_article, 
    create_or_update_article,
    ArticleListView, 
    ArticleDetailView, 
    ArticleCreateUpdateView,
    UserRegistrationView,
    UserLoginView,
    UserVerificationView,
    ResendVerifyEmailView,
    )

app_name = "board_mini"

urlpatterns = [
    path('hello/<to>', hello),
    
    # path('article/', list_article),
    # path('article/create/', create_or_update_article, {'article_id': None}), # {'article_id':None} 필수
    # path('article/<article_id>/', detail_article),
    # path('article/<article_id>/update/', create_or_update_article),    

    path('article/', ArticleListView.as_view()),
    path('article/create/', ArticleCreateUpdateView.as_view()),
    path('article/<article_id>/', ArticleDetailView.as_view()),
    path('article/<article_id>/update/', ArticleCreateUpdateView.as_view()),
    
    path('user/create/', UserRegistrationView.as_view()),
    path('user/login/', UserLoginView.as_view()),         # 로그인
    path('user/<pk>/verify/<token>/', UserVerificationView.as_view()), #인증 링크 검증
    path('user/resend_verify_email/', ResendVerifyEmailView.as_view()),
    path('user/logout/', LogoutView.as_view()),
]