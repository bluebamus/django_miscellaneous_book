"""django_basic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static

# namespace는 app의 urls에만 선언하는 것을 추천함
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('users', include('users.urls',namespace='users')),
    path('boardmini/', include('board_mini.urls')),
    path('users/', include('users.urls')),
    path('log/', include('log_test.urls')),
    path('naveroauth/', include('naver_oauth.urls')),
    path('basicskills/', include('basic_skills.urls')),
] 

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    