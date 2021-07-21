from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models_ex.models_signals_post_save import UserProfile


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(
            user=instance,
        )


'''

@ signals 모듈로 따로 분리할 경우 아래와 같이 apps.py와 __init__.py 설정을 따로 해줘야 한다.


# users/apps.py

from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    name = "users"

    def ready(self):
        from users.signals.post_save import post_save_user



 # users/__init__.py

default_app_config = "users.apps.UsersAppConfig"       

'''