from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser

UserModel = get_user_model()


# NaverBackend 백엔드는 기본인증백엔드(ModelBackend) 를 상속받아 대부분의 기능들을 그대로 사용합니다. 
# authenticate 메소드에서 비밀번호를 비교하여 인증하는 부분이 있는데 
# 이 부분을 삭제하고 소셜로그인으로 email 만 비교하도록 했습니다.

# 저는 예전에 naverid 도 데이터베이스에 저장하고 email 과 naverid 도 같이 비교하도록 구현한 적이 있는데 
# naverid 가 서비스에 필요하다면 저장하는 것이 맞으나 불필요하다면 굳이 데이터베이스에 저장할 필요는 없습니다. 

# 만일 email이 사용자 테이블에 존재하지 않는다면 None 을 반환해주면 됩니다. 
# 함수에서 아무것도 반환하지 않으면 None 을 리턴하므로 
# 사용자 데이터 검색에 실패할 경우 아무것도 하지 않도록(pass) 했습니다.

class NaverBackend(ModelBackend):
    def authenticate(self, request, username=None,**kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            pass
        else:
            # 사용자 데이터의 is_active 가 True 인지 확인하는 기능을 제공합니다. 
            # 비밀번호와 관계가 없으니 이것을 확인하는 것으로 인증백엔드의 인증테스트를 종료합니다.
            if self.user_can_authenticate(user):
                return user
