from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phonenumber = models.CharField(
        max_length=16,
        blank=True,
        null=True,
    )

    address = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )

# post_save_user는 User 모델이 생성될 때 실행하는 함수로 자동으로 UserProfile 모델을 생성해준다.

# post_save signal 은 sender, instance, created 등의 인자를 보내기 때문에 
# post_save_user 파라미터로 위와 같이 설정한다. 공식 문서에 따르면 
# def post_save_user(sender, **kwargs): 라 해도 똑같이 동작한다.

# post_save.connect 는 model(User)과 post_save_user 함수를 연결해 준다.

def post_save_user(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(
            user=instance,
        )

post_save.connect(post_save_user, sender=User)


# * tasks의 signals_post_save로 파일 분리 관리시의 예제가 있음, 한 곳에서 사용할 시 상관없음

# post_save.connect 대신 receiver 데코레이터를 사용할 수 있다.

# from django.dispatch import receiver

# @receiver(post_save, sender=User)
# def post_save_user(sender, instance, created, **kwargs):
#     if created:
#         user_profile = UserProfile.objects.create(
#             user=instance,
#         )