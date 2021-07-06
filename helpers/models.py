from django.db import models
from django.utils import timezone

""" 
from datetime import datetime
해당 함수는 UTC 기준으로 동작
settings.py의 USE_TZ = True가 되어 있으면 워닝이 발생함 때문에 아래와 같이 사용
"""


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True
        # 추상클래스 만들 경우 선언함

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
