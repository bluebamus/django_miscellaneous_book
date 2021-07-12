from django.conf import settings
from django.contrib.auth import login

import requests

class SingletonInstane:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance


class NaverClient(SingletonInstane):
    client_id = settings.NAVER_CLIENT_ID
    secret_key = settings.NAVER_SECRET_KEY
    grant_type = 'authorization_code'

    auth_url = 'https://nid.naver.com/oauth2.0/token'
    profile_url = 'https://openapi.naver.com/v1/nid/me'

    # singleton 이라는 패턴 사용
    # 첫번째 생성자 호출 때만 객체만 생성시키고 이후 생성자 호출부터는 먼저 생성된 객체를 공유하게 하는 방식

    # NaverClient 클래스를 NaverLoginMixin 뿐만 아니라 다른 클래스에서도 공유하며 사용할 수 있습니다. 
    # NaverClient 객체는 인스턴스변수가 없기 때문에 하나의 객체를 서로 공유하더라도 문제가 발생하지 않습니다.
    # 이렇게 인스턴스변수가 존재하지 않으나 여러 클래스에서 유틸리티처럼 사용하는 클래스의 경우 
    # 싱글턴 패턴을 많이 사용합니다. 
    # 객체를 생성하는 비용이 줄어 서버의 가용성을 높이는 좋은 패턴이며 가장 간단한 방법을 구현함

    # * 일반적으로 싱글턴은 생성자가 아니라 명시적으로 getInstance 라는 static 메소드를 제공해서 객체를 생성합니다. 
    # getInstance 를 사용하지 않고 생성자를 사용해 객체를 생성하면 에러를 발생시켜 
    # 싱글턴으로 구현되었음을 개발자에게 알려주는 것이죠. 
    # 원래 싱글턴 객체에 인스턴스변수를 추가하거나 클래스변수를 변경하면 안됩니다.

    # __instance = None

    # @classmethod
    # def __getInstance(cls):
    #     return cls.__instance

    # @classmethod
    # def instance(cls, *args, **kargs):
    #     cls.__instance = cls(*args, **kargs)
    #     cls.instance = cls.__getInstance
    #     return cls.__instance

    # def __new__(cls, *args, **kwargs):
    #     if not isinstance(cls.__instance, cls):
    #         cls.__instance = super().__new__(cls, *args, **kwargs)
    #         # cls.__instance = object.__new__(cls, *args, **kwargs)
    #     return cls.__instance


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    '''
     get_profile 메소드에서 headers 라는 파라미터가 사용되는데 
     http 헤더의 값을 딕셔너리 형태로 전달하면 됩니다. 
     
     Authorization 헤더를 token_type(bearer) 와 인증토큰을 조합한 값으로 추가했습니다. 
     각 함수 반환데이터는 json 메소드를 통해 본문의 내용을 딕셔너리 형태로 반환해 줄 수도 있습니다. 
     
     물론 본문이 json 타입이 아닐 경우 에러가 발생합니다.
    '''

    def get_access_token(self, state, code):
        res = requests.get(self.auth_url, params={'client_id': self.client_id, 'client_secret': self.secret_key,
                                                  'grant_type': self.grant_type, 'state': state, 'code': code})

        return res.ok, res.json()

    def get_profile(self, access_token, token_type='Bearer'):
        res = requests.get(self.profile_url, headers={'Authorization': '{} {}'.format(token_type, access_token)}).json()

        if res.get('resultcode') != '00':
            return False, res.get('message')
        else:
            return True, res.get('response')


# NaverLoginMixin 에서 네이버의 api를 구현한 네이버 클라이언트를 naver_client 클래스변수로 추가했습니다. 
# 네이버의 인증토큰 발급과 프로필 정보를 가져오는 두 가지의 기능을 제공합니다.

'''
naver_client로부터 token_infos 객체를 전달받는데 token_infos 객체는 아래와 같은 키를 갖는 딕셔너리 객체입니다.

1. error - 에러코드
2. error_description - 에러메시지
3. access_token - 인증토큰
4. refresh_token - 인증토큰 재발급토큰
5. expires_in - 인증토큰 만료기한(초)
6. token_type - 인증토큰 사용하는 api 호출시 인증방식(Authorization 헤더 타입)
'''
class NaverLoginMixin:
    naver_client = NaverClient.instance()

    def login_with_naver(self, state, code):
        
        # 인증토근 발급
        is_success, token_infos = self.naver_client.get_access_token(state, code)

        if not is_success:
            return False, '{} [{}]'.format(token_infos.get('error_desc'), token_infos.get('error'))

        access_token = token_infos.get('access_token')
        refresh_token = token_infos.get('refresh_token')
        expires_in = token_infos.get('expires_in')
        token_type = token_infos.get('token_type')

        # 네이버 프로필 얻기
        is_success, profiles = self.get_naver_profile(access_token, token_type)
        if not is_success:
            return False, profiles

        # 프로필정보까지 정상적으로 받아오면 사용자 모델에서 get_or_create 메소드를 통해 
        # 동일한 이메일의 사용자가 있는 지 확인 후 없으면 새로 생성합니다. 
        
        # 소셜로그인은 가입과 로그인을 동시에 제공하는 것이 더 좋습니다. 
        # 이미 가입되어 있는 사용자라면 회원정보(이름)만 수정하면 되고, 
        # 가입되어 있지 않은 케이스라면 새로 회원정보를 생성해서 가입시켜 줍니다. 

        # 소셜로그인은 로컬 비밀번호가 필요없기 때문에 새로 사용자 데이터가 추가되는 경우라면 
        # set_password(None) 메소드를 통해 랜덤한 비밀번호를 생성해서 저장합니다. 

        # 이미 소셜로그인을 통해서 이메일에 대한 인증도 되었으니 is_active 값도 활성화 시켜주고 
        # 저장을 하면 가입이 완료입니다. 

        # 만일 이미 가입되어 있던 사용자라면 이메일과 비밀번호로도 로그인이 가능하고 
        # 네이버 소셜로그인으로도 로그인이 가능합니다.

        # 사용자 생성 또는 업데이트
        user, created = self.model.objects.get_or_create(email=profiles.get('email'))
        if created: # 사용자 생성할 경우
            user.set_password(None)
        user.username = profiles.get('name')
        user.is_active = True
        user.save()

        # 가입된 이후에 로그인처리까지 해줘야 합니다. 
        # 로그인은 auth 프레임워크의 login 함수를 이용합니다. 
        # login 함수는 사용자 데이터와 로그인처리를 해줄 인증백엔드의 경로가 필요합니다. 
        # 기본 인증모듈인 'django.contrib.auth.backends.ModelBackend' 는 username(email) 과 비밀번호를 이용해서 
        # 인증처리를 하는데 소셜로그인은 비밀번호를 전달받을 수가 없습니다. 
        # 어쩔 수 없이 소셜로그인을 위한 인증백엔드를 추가로 구현해줘야 합니다.
        
        # 로그인
        login(self.request, user, 'naver_oauth.user.oauth.backends.NaverBackend')  # NaverBackend 를 통한 인증 시도
        # login(self.request, user, NaverBackend)

        # 소셜로그인의 마지막은 세션정보에 인증토큰정보를 추가하는 것입니다. 
        # 현재는 인증토큰이 필요없지만 네이버 api를 이용한 기능을 제공할 경우도 있습니다. 
        # 이 때 사용자의 인증토큰이 있어야만 사용자의 권한으로 네이버 서비스 api 기능들을 제공할 수 있는데 
        # 매번 재로그인을 할 수 없으니 인증토큰과 그 외 정보들을 세션에 저장합니다. 
        # 인증토큰 재발급토큰(refresh_token)도 함께 저장을 해야 인증토큰이 만료가 되더라도 
        # 재발급토큰으로 다시 인증토큰을 갱신할 수 있습니다. 
        # 만일 재발급토큰도 만료가 되었거나 문제가 있어서 인증토큰을 갱신할 수 없다면 로그아웃 처리 해주면 됩니다.

        # 세션데이터 추가
        self.set_session(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type)

        return True, user


        # 인증토큰이 정상적으로 발급되었다면 회원가입을 위해 이메일과 사용자의 이름을 받아야 하는데, 
        # 네이버에서 profile api도 제공해주기 때문에 이것을 이용해서 받아오면 됩니다.

        # get_naver_profile 메소드는 api를 통해 받아 온 프로필 정보를 검증하는 역할을 합니다. 
        # 프로필 정보는 사용자가 제공항목에 선택한 값들과 사용자의 id 값만 전달되는데 
        # 만일 이메일이나 이름을 선택하지 않은 경우 에러메시지를 반환하도록 했습니다.

    def get_naver_profile(self, access_token, token_type):
        is_success, profiles = self.naver_client.get_profile(access_token, token_type)

        if not is_success:
            return False, profiles

        for profile in self.required_profiles:
            if profile not in profiles:
                return False, '{}은 필수정보입니다. 정보제공에 동의해주세요.'.format(profile)

        return True, profiles

# 네이버의 api를 호출할 때 requests 라이브러리를 사용하여 호출하도록 했습니다. 
# requests 는 파이썬의 표준 http 클라이언트보다 사용하기 간편하고, 무엇보다 직관적입니다. 
# requests 라이브러리를 먼저 설치하세요.

# pip install requests

# reference : https://developers.naver.com/docs/login/web/web.md

# requests 모듈의 사용법을 알려드리면 get, post, put, delete 등의 함수들이 구현되어 있고, 
# 각각의 함수는 함수명과 동일한 http 메소드로 요청을 합니다. 
# 첫번째 위치 인자는 url 이고 그 외 파라미터는 keyword 인자로 전달하면 됩니다. 

# get_profile 메소드에서 headers 라는 파라미터가 사용되는데 
# http 헤더의 값을 딕셔너리 형태로 전달하면 됩니다. 
# Authorization 헤더를 token_type(bearer) 와 인증토큰을 조합한 값으로 추가했습니다. 
# 각 함수 반환데이터는 json 메소드를 통해 본문의 내용을 딕셔너리 형태로 반환해 줄 수도 있습니다. 
# 물론 본문이 json 타입이 아닐 경우 에러가 발생합니다.

