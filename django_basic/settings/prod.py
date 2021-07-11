from .base import *
from decouple import config


"""
export DJANGO_SETTINGS_MODULE=django_basic.settings.dev
export DJANGO_SETTINGS_MODULE=django_basic.settings.prod
"""

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(ROOT_DIR, "db.sqlite3"),
    }
}

DEBUG = False

ALLOWED_HOSTS = ["*"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

'''
STATIC_URL: 이 경로로 시작되는 요청은 static 핸들러로 라우팅
STATIC_ROOT: collectstatic 커맨드로 static 파일들을 모을 때 저장될 디렉토리 경로
STATICFILES_DIRS: collectstatic 또는 findstatic 커맨드 실행시 검색하는 디렉토리 경로들의 리스트. 
주로 앱 내부의 static 디렉토리가 아닌 다른 곳에 저장되어 있을 경우 설정함.
STATIC_ROOT 는 현재 존재하는 디렉토리 경로를 설정해야 합니다. 윈도우는 예외이지만 리눅스 
또는 맥에서는 manage.py 를 실행하는 권한으로 디렉토리 권한이 설정되어 있어야 합니다.
(웹서버에서 static 파일을 직접 전송해야 한다면 웹서버에서 읽을 수 있어야 합니다.) 


부모 블록의 내용을 완전히 덮어쓰지 않고 일부만 추가하고자 할때는 {{ block.super }}를 사용.
{% endblock %}에 태그 이름 붙이기. > {% endblock content%}: 가독성 용이.

'''

STATIC_URL = "/static/"
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     STATIC_DIR,
# ]

# static url로 접근했을 때 연결되는 위치 정의
# static 파일을 한 곳에 모아서 서비스 할 경위 상위 STATICFILES_DIRS 변수는 불필요함

STATIC_ROOT = os.path.join(ROOT_DIR, "static")

# python manage.py collectstatic

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(ROOT_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
