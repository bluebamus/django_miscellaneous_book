
from django.conf import settings
# from django.middleware.csrf import _compare_salted_tokens 함수명 변경됨
from django.middleware.csrf import _compare_masked_tokens
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from naver_oauth.user.oauth.providers.naver import NaverLoginMixin


# 뷰는 화면이 필요없고 오직 서버단에서 네이버 인증토큰을 받고 인증처리를 하는 기능만 합니다. 
# 그래서 기본 제네릭뷰를 상속받았습니다. 로그인에 설정할 경우 
# settings.LOGIN_REDIRECT_URL 로 이동하고 로그인에 실패할 경우 settings.LOGIN_URL 에 이동하도록 설정했습니다. 

# * board_mini와 분리했기 때문에 로그인에 성공 및 실패할 경우 url은 view에서 정의함

# 만일 변경하고 싶으시다면 success_url, failure_url 클래스변수를 수정하시면 됩니다.
# (해당 값들은 설정파일에 설정하는 것이 재사용하는 데 편리합니다.)


'''
여기서는 앱을 분리하지 않고 조금 복잡하지만 소셜로그인과 사용자 앱을 하나의 앱으로 관리할 예정입니다. 
하나의 앱으로 관리하면 좋은 점은 소셜로그인 기능이 사용자 모델에 어느정도 의존성이 있기 때문에 
문제의 여지가 줄어듭니다. 

예를들어 장고 auth 프레임워크에서 기본으로 제공하는 사용자 모델은 사용자의 이름이 
first_name, last_name 으로 분리되어 있으나
새로운 사용자 모델에서는 name 이라는 하나의 필드로만 제공하고, 
소셜로그인할 때도 name 이라는 필드를 사용합니다. 

만일 사용자 모델에 name 이라는 필드가 없다면 오류가 생길테니 NaverLoginMixin 을 수정해주셔야 합니다. 
email 필드의 이름이 변경될 경우도 마찬가지이구요.
'''

class SocialLoginCallbackView(NaverLoginMixin, View):

    # success_url = settings.LOGIN_REDIRECT_URL
    # failure_url = settings.LOGIN_URL
    success_url = '/naveroauth/user/login/'
    failure_url = '/naveroauth/user/login/'
    required_profiles = ['email', 'name']
    model = get_user_model()

    def get(self, request, *args, **kwargs):        
        provider = kwargs.get('provider')
        success_url = request.GET.get('next', self.success_url)

        if provider == 'naver':
            csrf_token = request.GET.get('state')
            code = request.GET.get('code')
            if not _compare_masked_tokens(csrf_token, request.COOKIES.get('csrftoken')):
                messages.error(request, '잘못된 경로로 로그인하셨습니다.', extra_tags='danger')
                return HttpResponseRedirect(self.failure_url)
            is_success, error = self.login_with_naver(csrf_token, code)
            if not is_success:
                messages.error(request, error, extra_tags='danger')
            return HttpResponseRedirect(success_url if is_success else self.failure_url)

        return HttpResponseRedirect(self.failure_url)

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value