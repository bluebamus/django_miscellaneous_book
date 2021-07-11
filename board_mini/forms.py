from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import EmailField
from .validators import RegisteredEmailValidator

# email 필드를 정상적인 email 형식의 input 태그로 변경하겠습니다. 
# 굳이 하지 않아도 문제가 없지만 email 형식으로 변경하면 
# 모바일에서 자판이 email 용으로 나타나는 장점이 있습니다. 
# 
# 템플릿은 그대로 두고 폼클래스를 수정해서 CharField로 선언된 부분을 EmailField로 변경해줍니다.

'''
LoginView 에서 form_class 로 설정된 AuthenticationFrom 을 상속받아 LoginForm 이라는 폼클래스를 정의하고, 
username 이라는 클래스를 EmailField로 변경하고 내부의 widget을 EmailInput으로 변경합니다.
'''

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username')


# Field와 Widget의 역할이 궁금하실 수 있는데 
# Field는 유효성 검증과 위젯의 기능들을 호출하는 역할을 합니다. 
# Widget은 필드의 실제 렌더링과 관련된 역할을 합니다. 
# Widget에 따라 input_type 클래스변수에 email 인지 text 인지 password 인지가 정의되어 있습니다.

class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))


# 도메인 mx를 확인하고 이메일이 존재하는지 확인하려면 validate_email과 함께 pyDNS 패키지를 설치할 수 있습니다.
# 이미 인증된 이메일이나, 가입된 적 없는 이메일이 입력된 경우 에러를 발생시키는 기능을 합니다.
# * 에러메시지를 필드에 표시하기 위해 뷰가 아닌 필드에서 유효성을 검증하도록 했습니다.

# 유효성 검증필터는 EmailField 의 기본 필터에 추가하기 위해서 
# RegisteredEmailValidator() 인스턴스를 default_validators 리스트에 추가했습니다.
# 이메일 형식 검사 + DB에 등록된 사용자인지 검사

class VerificationEmailForm(forms.Form):
    email = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), validators=(EmailField.default_validators + [RegisteredEmailValidator()]))
