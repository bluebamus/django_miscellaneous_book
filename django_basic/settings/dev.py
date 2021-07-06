from .base import *
from decouple import config


"""
export DJANGO_SETTINGS_MODULE=django_basic.settings.dev
export DJANGO_SETTINGS_MODULE=django_basic.settings.prod
"""

# debug toolbar를 동작시키기 위한 서버 ip 정보를 명시함
INTERNAL_IPS = [
    "127.0.0.1",
    "0.0.0.0",
]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
]


def custom_show_toolbar(self):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "ENABLE_STACKTRACES": True,
    "SHOW_TOOLBAR_CALLBACK": custom_show_toolbar,
}

INSTALLED_APPS += [
    "debug_toolbar",
    'django_nose',    
    ]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TEST_OUTPUT_DIR = os.environ.get('TEST_OUTPUT_DIR', '.')

# NOSE_ARGS = [
#     '--verbosity=2',
#     '--nologcapture',
#     '--with-coverage',
#     '--cover-package=app1,app2,app3',
#     '--with-spec',
#     '--spec-color',
#     '--with-xunit',
#     '--xunit-file=%s/unittests.xml' % TEST_OUTPUT_DIR,
#     '--cover-html',
#     '--cover-xml',
#     '--cover-xml-file=%s/coverage.xml' % TEST_OUTPUT_DIR,
#     "--exe",
# ]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(ROOT_DIR, "db.sqlite3"),
    }
}

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_DIR = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    STATIC_DIR,
]

# static url로 접근했을 때 연결되는 위치 정의
# static 파일을 한 곳에 모아서 서비스 할 경위 상위 STATICFILES_DIRS 변수는 불필요함

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
