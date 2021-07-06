# User 모델 클래스 획득 방법

## 1) 좋지 않은 방법 : global setting 오버라이딩을 통해서 인증 User 모델을 다른 모델로 변경할 수 있음
from django.contrib.auth.models import User

User.objects.all()


## 2) get_user_model helper 함수를 통해 모델 클래스 참고 (추천)
from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.all()


## 3) settings.AUTH_USER_MODEL 을 통한 모델클래스 참조 (추천)
from django.conf import settings # 추천!
from django.contrib.auth.models import User # 비추
from django.db import models

class Post(models.Model):
	author = models.ForeignKey(User) 		# 비추
	author = models.ForeignKey('auth.User') # 비추
	author = models.ForeignKey(settings.AUTH_USER_MODEL) # 추천!

# User 모델의 확장 여러 가지 기법
## 프록시 모델 사용하기
## User 모델과 일대일관계의 프로필 테이블 추가하기
## AbstractUser 모델 상속한 사용자 정의 User 모델 사용하기
## AbstractBaseUser 모델 상속한 사용자 정의 User 모델 사용하기

# ------------------------------------------------------------

# 프록시 모델 사용하기

## 프록시 모델이란 새 테이블을 추가하는 등의 데이터베이스 스키마 변경 없이 단순히 상속한 클래스이다.
## 정렬순서 같은 기존 모델의 동작을 변경하거나 새로운 메소드를 추가하기 위해 사용한다.
## 데이터베이스에 부가적인 사용자 정보를 저장할 필요가 없을 때 사용하는 방법이다.

from django.contrib.auth.models import User
# User.objects.all()과 Person.objects.all() 코드는 스키마의 변경이 없으므로 같은 쿼리로 동작한다.
class ProxyUser(User):  
    objects = User.objects.all()
    #objects = PersonManager()

    class Meta:
        proxy = True
        ordering = ('-username',)

    # def do_something(self): 형식의 메소드 추가 가능
    def do_print(self):
        for username in self.objects:
            print("Hello! " + username.__str__())
