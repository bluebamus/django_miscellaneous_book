"""
Django settings for django_basic project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from decouple import config
from os.path import join

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = os.path.dirname(BASE_DIR)
TEMPLATE_DIR = os.path.join(ROOT_DIR, "templates")
# APPS_DIR = os.path.join(BASE_DIR, 'apps')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "helpers",
    #'users', # board_mini AbstractBaseUser user와 충돌
    "log_test",
    "models_example",
    "board_mini",
    "naver_oauth",
    "basic_skills",
    "django.contrib.sites",  # 사이트맵 라이브러리 추가
    "django.contrib.sitemaps",  # 사이트맵 라이브러리 추가
    "orm_skills",
]


# 인증백엔드는 NaverLoginMixin 에서 사용을 하지만 이것은 로그인을 시도할 때 어떤 백엔드를 사용할 지에 대한 설정입니다.

# 이후 로그인된 상태에서 또다른 요청을 할 때 장고는 세션의 정보를 확인하여 로그인된 사용자가 맞는지,
# 맞다면 어떤 사용자인지를 식별하는데 장고의 기본값인 기본인증백엔드를 통해 식별처리를 실행합니다.

# 소셜로그인으로 로그인 사용자를 위해 설정파일의 AUTHENTICATION_BACKENDS 변수에 NaverBackend 를 추가합니다.

# AUTHENTICATION_BACKENDS는 설정은 세션의 사용자 정보를 식별할 때 사용될 백엔드를 리스트로 설정하여
# 실제 사용자 정보를 식별할 때 리스트의 순서대로 백엔드에 인증을 시도하고,
# 인증이 되면 해당 인증된 사용자 정보를 넘겨주고, 인증에 실패할 경우 리스트의 다음 백엔드에 위임하게 됩니다.
# 모든 백엔드에서 인증에 실패할 경우 인증되지 않은 사용자라고 처리하는 것이죠.


# 가장 많은 사용자가 이용하는 백엔드를 가장 위에 설정하고,
# 가장 사용하지 않는 백엔드를 가장 밑에 설정하는 것이 인증 성능을 높이는 한가지 포인트라고 할 수도 있습니다

AUTHENTICATION_BACKENDS = [
    "naver_oauth.user.oauth.backends.NaverBackend",  # 네이버 인증백엔드
    "django.contrib.auth.backends.ModelBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_basic.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_basic.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

"""
UserAttributeSimiarityValidator 는 사용자 모델의 속성(즉, 필드)와 비교해서 유사한 경우 
오류를 발생시키는 유틸리티입니다. 

기본으로 비교하는 필드는 정해져 있지만 수정이 가능합니다. 
username, first_name, last_name, email 이 네 가지를 비교하는데 email을 제외하고 
나머지 3개의 필드들은 새로운 사용자 모델에서 삭제했었죠. 

그러니 email과 name 두 가지의 필드를 user_attributes 이라는 이름의 옵션으로 전달해주면 됩니다. 

또한 유사도를 나타내는 max_similarity 옵션도 있지만 기본값으로 0.7이라는 값이 설정되어 있는데
굳이 변경할 필요가 없어 보입니다. 
validator에 옵션을 전달하는 방법은 설정파일의 AUTH_PASSWORD_VALIDATORS 변수에 옵션을 전달해주면 됩니다.
{

    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',

    'OPTION': {'user_attributes': ('email', 'name')},
},
"""

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = False  # true로 선택하면 UTC 기준으로 시간이 저장됨, True로 설정하고 다른 시간 함수로만으로 제어도 가능함
# ref : https://it-eldorado.tistory.com/13

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 기본 로그인 페이지 URL 지정
# login_required 장식자 등에 의해서 사용

# 기본형
# LOGIN_URL = "/login/"

# board_mini 설정
LOGIN_URL = "/boardmini/user/login/"

# 로그인 완료 후 next 인자가 지정되면 해당 URL 페이지로 이동
# next 인자가 없으면 아래 URL로 이동

# 기본형
# LOGIN_REDIRECT_URL = "/"

# board_mini 설정
LOGIN_REDIRECT_URL = "/boardmini/article/"


# 로그아웃 후에 next 인자기 지정되면 해당 URL 페이지로 이동
# next 인자가 없으면 LOGOUT_REDIRECT_URL로 이동
# LOGOUT_REDIRECT_URL이 None(디폴트)이면, 'registration/logged_out.html' 템플릿 렌더링
# LOGOUT_REDIRECT_URL = None
LOGOUT_REDIRECT_URL = "/boardmini/article/"

# 인증에 사용할 커스텀 User 모델 지정 : '앱이름.모델명'
# user app test 사용
# AUTH_USER_MODEL = 'users.User'
AUTH_USER_MODEL = "board_mini.User"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Email 관련 설정
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

# 소셜 로그인
NAVER_CLIENT_ID = config("NAVER_CLIENT_ID")
NAVER_SECRET_KEY = config("NAVER_SECRET_KEY")

# SEO Sitemap 만들기
SITE_ID = 1  # ㅇ

# server_time - 서버의 시간
# asctime - 현재 시간

# disable_existing_loggers : True일 경우 기본 구성의 logger들이 비활성화된다.

# file 핸들러
# 'filters': ['require_debug_false'],  디버그모드가 False일때만 작동합니다
# class - 파일 핸들러로 RotatingFileHandler 사용, RotatingFileHandler는
# 파일 크기가 설정한 크기보다 커지면 파일 뒤에 인덱스를 붙여서 백업한다.
# 이 핸들러의 장점은 로그가 무한히 증가되더라도 일정 개수의 파일로 롤링(Rolling)되기 때문에
# 로그 파일이 너무 커져서 디스크가 꽉 차는 위험을 방지할 수 있다.
# backupCount - 롤링되는 파일의 개수를 의미한다. 총 5개의 로그 파일로 유지
# 'maxBytes': 1024*1024*5,  # 5 MB

# 두 class 중 하나를 사용하는듯
# 'class': 'logging.handlers.RotatingFileHandler', -> 파일 용량을 정해서 log를 쌓고 제거할 때
# 'class': 'logging.FileHandler', -> 로그를 계속 쌓고 싶을 때
# TimedRotatingFileHandler -> 시간을 정해서 log를 쌓고 제거할 때

# style 은 %, 〈{〈 또는 〈$〉 중 하나

# style 이 〈%〉 이면, 메시지 포맷 문자열은 %(<dictionary key>)s 스타일의 문자열 치환을 사용
# - 가능한 키 확인 : https://docs.python.org/ko/3/library/logging.html#logrecord-attributes
# style이 〈{〈 인 경우 메시지 포맷 문자열은 str.format()(키워드 인자 사용)과 호환되는 것으로 가정
# 스타일이 〈$〉 이면 메시지 포맷 문자열은 string.Template.substitute() 가 기대하는 것과 일치

# 주요 기능 참고
# https://docs.python.org/ko/3/howto/logging.html

# 고급 설정 참고
# https://runebook.dev/ko/docs/django/topics/logging
# https://djangodeconstructed.com/2018/12/18/django-and-python-logging-in-plain-english/

"""
윈도우 테스트시 debug level 출력 안됨, 파일 출력 안됨
차후 버그 픽스
"""

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "datefmt": "%d/%b/%Y %H:%M:%S",
            "style": "{",
        },
        "standard": {
            "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": join(ROOT_DIR, "logs/logfile.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "standard",
        },
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "django.server": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
