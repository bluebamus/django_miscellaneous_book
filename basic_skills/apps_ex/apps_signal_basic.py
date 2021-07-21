from django.apps import AppConfig

from django.core.signals import request_started
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from ..tasks.signal_basic_log_tasks import (
    log_request,
    log_request_adv,
    save_or_create_user_profile,
)


class BasicSkillsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "basic_skills"

    # Now every time a request comes into the application,
    # the message "New Request!" will be logged in stdout.

    def ready(self):
        # request_started.connect(log_request)
        request_started.connect(log_request_adv)

        # 이번에는 함수를 post_save 신호에 연결할 때 보낸 사람 인수를 전달합니다.

        # 이것은 우리의 save_or_create_user_profile 함수가 post_save 신호의 발신자가 사용자 모델인 경우에만
        # 호출된다는 것을 의미합니다.

        # 이것은 또한 우리가 서로 다른 작업을 수행하기 위해 서로 다른 코드를 실행하는
        # 다양한 모델과 함께 post_save 신호에 연결할 수 있음을 의미합니다.

        post_save.connect(save_or_create_user_profile, sender=User)
