# AbstractUser 모델 상속한 사용자 정의 User 모델 사용하기

## AbstractUser 모델을 상속한 User 모델을 만들어 settings.py에 참조를 수정해야 한다. 
## 이 기법의 사용 여부는 프로젝트 시작 전에 하는 것이 좋다. 추후에 settings.AUTH_USER_MODEL 변경시 데이터베이스 스키마를 알맞게 재수정해야 하는데 사용자 
## 모델 필드에 추가나 수정으로 끝나지 않고 완전히 새로운 사용자 객체를 생성하는 일이 된다.
## 이 기법은 기존 Django의 User 모델을 그대로 사용하므로 기본 로그인 인증 처리 부분은 Django의 것을 이용하면서 몇몇 사용자 정의 필드를 추가할 때 유용하다.
#
## 완전히 새로운 사용자 모델을 만듭니다. 
## 당연히 세심한 주의를 필요로 합니다. 프로젝트의 영향도 AbstracBaseUser를 사용한 확장 방식과 비슷합니다. 
## 이런 짓은 프로젝트 초반에 해야하고, 지금 해야겠다면 리뉴얼 할 수 있는 기간을 확보하세요. 
## 당연히 테스트 코드도 다시 작성해야 합니다(그러니 기획자를 설득합시다).
#
## 이걸 사용해야 하는 이유는 인증 프로세스에 특별한 요구사항이 없는데(!), 
## 추가 클래스를 만들 필요없이 사용자 모델에 직접 추가 정보를 추가하려고 할 때 사용하면 됩니다
## (One-To-One을 사용해서 확장하는 방법을 왜 사용하지 않는지 궁금하지만 여튼 그럴때 사용합니다).

# models
from django.db import models  
from django.contrib.auth.models import AbstractUser


class AUUser(AbstractUser):  
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

'''
settings.py에 추가

# 사용자 인증에 사용될 모델 명시 '앱이름.모델이름'

AUTH_USER_MODEL='users.AUUser'

# INTALLED_APPS에 앱 이름 추가

INSTALLED_APPS=[
  ...
  'users',
]
'''