# AbstractBaseUser 모델 상속한 사용자 정의 User 모델 사용하기

## AbstractBaseUser 모델을 상속한 User 모델을 만들고 settings.py에 참조를 수정하는 것은 AbstractUser 모델을 상속하는 것과 같다. 
## 따라서 마찬가지로 프로젝트 시작 전에 이 기법의 사용 여부를 결정하는 것이 바람직하다.
#
## 그런데 AbstractUser 모델을 상속하는 방법과 달리 로그인 아이디로 이메일 주소를 사용하도록 하거나 
## Django 로그인 절차가 아닌 인증 절차를 직접 구현하고자 할 때 사용할 수 있다.

# * AbstractBaseUser 상속 뿐만 아니라 PermissionsMixin을 다중상속한다. Django의 기본 그룹, 허가권 관리 기능을 재사용한다.

# reference django doc : https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#a-full-example

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone

# 만약 커스텀한 user model이 장고의 기본 user model과 같다면 UserManager를 정의하면 된다. 
# 같지 않다면 create_user() 및 create_superuser() 메소드를 제공하는 BaseUserManager를 상속받아 
# create_user()와 create_superuser()를 정의해야 한다.

class UserManager(BaseUserManager):
    # 선택적으로 관리자를 마이그레이션으로 직렬화한다.
    # # True로 설정된 경우 관리자가 마이그레이션으로 직렬화된다고 하는데 더 상세 정보가 요구됨
    use_in_migrations = True  

    '''
    ref: https://wikidocs.net/6668
    
    모델 매니저를 메소드 체인로 지정하는 방식
    
    커스템 모델 매니저를 정의한다.
    class PublishedManager(models.Manager):
    # use_for_related_fields = True 옵션은 기본 매니저로 이 매니저를 정의한 모델이 있을 때 이 모델을 가리키는 모든 관계 참조에서 모델 매니저를 사용할 수 있도록 한다.
    use_for_related_fields = True

    def published(self, **kwargs):
        return self.filter(status='published', **kwargs)
    '''

    # 유저 생성
    # 파라미터로 전달받은 값들을 user 객체로 db에 저장한다
    # nomalize 중복 최소화를 위한 정규화?
    def _create_user(self, email, nickname, first_name, last_name, password, **extra_fields):
        # @도메인 에 대한 정규화만 진행, 소문자화

        eamil = self.normalize_email(email)
        
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            first_name=first_name,
            last_name=last_name,            
            **extra_fields
            )  
                
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, nickname, last_name, first_name, password=None, **extra_fields):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        if not email:
            raise ValueError(('Users must have an email address'))        
   
        return self._create_user(email, nickname, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, nickname, last_name, first_name, password=None, **extra_fields):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not email:
            raise ValueError(('Users must have an email address'))

        return self._create_user(email, nickname, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=('Email address'),
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(
        verbose_name=('Nickname'),
        max_length=30,
        unique=True
    )
    first_name = models.CharField(verbose_name=('first name'), max_length=30, blank=True)
    last_name = models.CharField(verbose_name=('last name'), max_length=150, blank=True)
    is_active = models.BooleanField(
        verbose_name= ('Is active'),
        default=True
    )
    is_superuser = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=(
            'Designates whether the user can log into this admin site.'
        ),
    )

    date_joined = models.DateTimeField(
        verbose_name=('Date joined'),
        default=timezone.now
    )
    # 이 필드는 레거시 시스템 호환을 위해 추가할 수도 있다.
    # salt 기법을 사용하기 위한 salt 키 값
    salt = models.CharField(
        verbose_name=('Salt'),
        max_length=10,
        blank=True
    )

    objects = UserManager()

    # 필수로 설정해줘야한다.
    # USERNAME_FIELD은 user model에서 사용할 고유 식별자, 기본은 id
    USERNAME_FIELD = 'email'

    EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS 는 createsuperuser 커맨드를 실행하여 관리자를 생성할 때 입력받을 필드
    REQUIRED_FIELDS = ['nickname', 'first_name', 'last_name']

    class Meta:
        db_table = "abstractbaseuser_user"
        verbose_name = ('user')
        verbose_name_plural = "users"        
        verbose_name_plural = ('users')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.nickname

    def get_full_name(self):        
        return self.nickname

    def get_short_name(self):
        return self.nickname

    # def has_perm(self, perm, obj=None):: True를 반환하여 권한이 있음을 알립니다. Ojbect를 반환하는 경우 해당 Object로 사용 권한을 확인하는 절차가 필요하다.
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    # def has_module_perms(self, app_label):: True를 반환하여 주어진 앱(App)의 모델(Model)에 접근 가능하도록 한다.
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # def is_staff(self):: True가 반환되면 장고(django)의 관리자 화면에 로그인 할 수 있습니다.
    # property 함수 명은 필드명과 동일하면 안된다 - form field에서 에러 발생
    @property
    def is_user_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_staff

    @property
    def is_user_superuser(self):
        "Is the user a admin member?"
        return self.is_superuser

    @property
    def is_user_active(self):
        "Is the user active?"
        return self.is_active

    # 해당 라인의 사용 목적 및 사용 방법 : https://github.com/wagtail/wagtail/issues/4320
    # admin에서 테이블 아이템명을 설정해준다.    
    get_full_name.short_description = ('Full name')