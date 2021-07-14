from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

# from views_messages import *
# from views_two_scoops_of_django import *
from .views_cbv_mixin import FlavorListView

# sitemap 설정
from django.contrib.sitemaps.views import sitemap
from .sitemap import BoardMiniSitemap

# 단일 html 파일을 만들고 static 파일에 저장하신 경우,
# from mysite import views as mysite_views
# from mysite.sitemaps import StaticViewSitemap

# config 폴더 사용을 추천
#from config.sitemaps import PytonBlogSitemap

# static 사용시 예제
# 참고 : https://surfinryu.blogspot.com/2020/04/python-django-sitemapxml.html

# sitemaps = {
#     'products': ProductSitemap,
#     'static': StaticViewStitemap,
# }

# ! xml 접근 및 출력은 되지만 sitemap 정보는 출력이 안됨 테스트가 더 필요함

sitemaps = {
    'board_mini':BoardMiniSitemap,     
}

app_name = "basic_skills"

# static을 넣으신 경우에는 사이트 주소를 추가해줍니다.
# path('assets/sites/about-us.html', mysite_views.about, name='about-us'),

# Static sites를 생성하신 경우에는 views에 따로 정의를 해줘야 합니다
# def about(request):
#    return render(request, 'static/sites/about-us.html') 

urlpatterns = [
    path('', FlavorListView.as_view()),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),    
]


# 참고 : https://pythonblog.co.kr/blog/46/
# 참고 : https://surfinryu.blogspot.com/2020/04/python-django-sitemapxml.html
# 참고 : https://enfanthoon.tistory.com/159