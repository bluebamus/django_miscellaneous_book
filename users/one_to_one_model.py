# User 모델과 일대일관계의 프로필 테이블 추가하기

## 기존 User 모델과 OneToOneField로 일대일관계를 맺는 Django 모델을 추가해서 사용자에 관한 정보를 저장하는 것이다.
## Django의 인증 시스템을 그대로 활용하고 로그인, 권한 부여 등과 상관이 없는 사용자 정보 필드를 저장하고자 할 때 사용하는 기법이다.
#
## 데이터베이스에 추가 정보를 담을 수 있는 테이블을 하나 생성하여 관리할 때 사용하는 방법입니다.
## 기본 모델을 유지하고, 인증 정보 수정없이 추가 정보를 저장하려고 할 때 사용하면 좋은 방법입니다.

from django.db import models  
from django.contrib.auth.models import User  

from django.db.models.signals import post_save  
from django.dispatch import receiver

class OneToOneUser(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE) # User 모델과 1:1관계
    email = models.EmailField(max_length=20, verbose_name='user email', blank=True)
    age = models.PositiveSmallIntegerField(max_length=30, verbose_name='age', blank=True)
    birth_date = models.DateField(null=True, verbose_name='birth date', blank=True)
