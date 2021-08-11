from django.shortcuts import render
from django.http import HttpResponse
import logging 
logger = logging.getLogger('django.server')

# logger = logging.getLogger('django') 이렇게 명시적으로 선언하면
# project/settings.py 의 LOGGING > loggers > django 의 내용을 사용한다는 뜻

# logger = logging.getLogger() 이렇게 사용하시면 warning 이상 출력합니다.
# logger = logging.getLogger(__name__) 을 사용할수도 있습니다. 해당 파일을 인자로 사용 할 수 있습니다.

# logger.log() : 특정 로그 수준의 로깅 메시지를 수동으로 생성합니다.
# logger.exception() : 현재 예외 스택 프레임을 래핑 하는 ERROR 레벨 로깅 메시지를 작성합니다.

# 표현식
# https://developpaper.com/2-django-advanced-logging-function/

def home(request):

    logger.debug("debug!!!")
    # logger.info('info!!!')
    # logger.warning('warning!!!')
    # logger.error('error!!!')
    # logger.critical('critical!!!')
    return HttpResponse('finish')
    # 생략