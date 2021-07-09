from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
#from .managers import UserManager


class UserBasicModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email', unique=True)
    username = models.CharField('이름', max_length=30, blank=True) # AbstractBaseUser의 name은 꼭 username로 명시해야 한다
    is_staff = models.BooleanField('스태프 권한', default=False)
    is_active = models.BooleanField('사용중', default=True)
    date_joined = models.DateTimeField('가입일', default=timezone.now)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'                     # email을 사용자의 식별자로 설정
    REQUIRED_FIELDS = ['username',]                   # 필수입력값

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'
        abstract = True

    def email_user(self, subject, message, from_email=None, **kwargs): # 이메일 발송 메소드
        send_mail(subject, message, from_email, [self.email], **kwargs)

'''
python3.6/site-packages/django/contrib/auth/models.py

 모델과 폼의 label에 해당하는 값들을 보시면 _('msgid') 형식으로 선언되어 있을 겁니다. 
예를 들어 모델에서 email 필드를 보시면 _('email address')로 선언되어 있습니다. 
이 _라는 함수는 ugettext_lazy 함수의 별칭(별명) 입니다. 

이 함수는 언어설정에 따라 출력되는 문자열을 변환해주는 함수입니다. 
설정파일의 LANGUAGE_CODE 만 변경시켜주면 장고에서 미리 번역해둔 문자열들로 치환되어 출력됩니다.

다국어 설정은 아무런 문자나 자동으로 변환(번역)이 되는 것이 아니라 
번역파일에 미리 정의 해놓은 문자들만 변환이 됩니다. msgid에 대응하는 문자들을 언어별로 작성해야 합니다. 
./manage.py 유틸리티의 makemessages 커맨드는 프로젝트내의 ugettext_lazy 함수의 인자들을 검색 후 
언어별로 번역파일을 생성합니다. 번역파일에 해당 msgid 에 대응하는 msgstr 을 정의해주면 번역파일이 생성이 되고, 
번역단어가 많고 여러 언어로 설정할 경우 검색하는 시간이 오래 걸려 전체적으로 서비스의 속도가 굉장히 저하됩니다.
 
그렇기 때문에 장고에서 읽기 편하게 미리 컴파일을 해둬야 하는데 
이것이 ./manage.py 유틸리티의 compilemessages 커맨드입니다. 
다국어 설정은 인싸가 되기 위해 중요하지만 여기서 길게 설명하지 않으니 
더 자세한 설명은 공식문서를 참고하시기 바랍니다.
'''
