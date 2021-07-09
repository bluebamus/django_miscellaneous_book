from django.urls import path
from .views import (
    hello, 
    list_article, 
    detail_article, 
    create_or_update_article,
    ArticleListView, 
    ArticleDetailView, 
    ArticleCreateUpdateView,
    UserRegistrationView
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
]