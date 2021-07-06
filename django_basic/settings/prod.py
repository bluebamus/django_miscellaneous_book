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
