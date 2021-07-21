import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

# reference : https://wikidocs.net/10566

"""
@receiver 데코레이터를 이용해 sig_user_logged_in() 함수 이름으로 
user_logged_in 시그널을 처리하는 함수를 만든다.

참고로 django/contrib/auth/__init__.py 파일의 
login(request, user, backend=None) 함수 맨 밑에 보면 로그인 작업을 완료한 후 시그널을 보내는 코드가 존재한다.

python user_logged_in.send(sender=user.__class__, request=request, user=user)

로그인할 때마다 이미 위와 같이 시그널을 보내고 있으므로 이를 수신하는 함수를 정의하면 된다.

시그널 수신 함수를 정의하고 이를 Django 앱 설정을 통해 아래의 코드로 등록해야 한다.
"""

from ipware.ip import get_ip
from ..models_ex.models_signal_login_ip_logging import UserLoginLog


@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    logger = logging.getLogger(__name__)
    logger.debug("user logged in: %s at %s" % (user, request.META["REMOTE_ADDR"]))

    # log = UserLoginLog()
    # log.user = user
    # log.ip_address = get_ip(request)
    # log.user_agent = request.META['HTTP_USER_AGENT']
    # log.save()


# 사용자 아이피 주소를 얻기 위해 request.META['REMOTE_ADDR'] 코드가 아닌
#  django-ipware 라이브러리를 사용한다.
