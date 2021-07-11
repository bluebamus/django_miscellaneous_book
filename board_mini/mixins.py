
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render

# from minitutorial import settings
from django.conf import settings

# 중복되는 메소드와 클래스변수를 mixin 에 선언하고, 
# 회원가입뷰와 인증이메일 재발송하는 뷰에서는 해당 mixin 을 추가하도록 하겠습니다.

# request.META는 사용자의 IP 주소와 사용자 Agent(일반적으로 웹 브라우저의 이름과 버전)를 포함해 
# 지정된 요청에 대해 사용할 수 있는 모든 HTTP 헤더가 들어있는 파이썬 딕셔너리다.

# HTTP_ORIGIN는 CSRF (Cross Site Request Forgery) 요청으로부터 보호하는 방법입니다
# 요청 헤더의 이름은 Origin입니다.
# 이 헤더는 CSRF에 대한 보호가 필요한 경우에만 전송됩니다
# reference : https://wiki.mozilla.org/Security/Origin
# 주의 : 일부 브라우저는 이러한 기능을 지원하지 않음

class VerifyEmailMixin:
    email_template_name = '/boardmini/user/email/registration_verification.html'
    token_generator = default_token_generator

    def send_verification_email(self, user):
        token = self.token_generator.make_token(user)
        url = self.build_verification_link(user, token)
        subject = '회원가입을 축하드립니다.'
        message = '다음 주소로 이동하셔서 인증하세요. {}'.format(url)
        html_message = render(self.request, self.email_template_name, {'url': url}).content.decode('utf-8')
        user.email_user(subject, message, from_email=settings.EMAIL_HOST_USER,html_message=html_message)
        messages.info(self.request, '회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.')

    def build_verification_link(self, user, token):
        return '{}/user/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)

'''
render 함수는 HttpResponse 객체를 반환합니다. HttpResponse 객체의 content 속성에 렌더링된 메시지가 저장되어 있는데
http로 전송할 수 있도록 byte 로 인코딩되어 있습니다. 

email_user 메소드에 전달할 때 반드시 utf-8 로 디코딩을 해줘야 합니다. 

email_user 메소드를 호출할 때 기존의 텍스트 메시지와 html 메시지 둘다 전달한 이유는 
일부 이메일 클라이언트에서는 html 형식의 이메일을 지원하지 않을 수 있어서
html 메시지를 보여줄 수 없는 이메일 클라이언트에게 기본적으로 보여줄 내용으로 텍스트 메시지를 전달하는 것이 좋습니다.

django.template.loader.render_to_string 함수를 이용하면 곧바로 렌더링된 utf-8 문자열을 출력합니다.
'''