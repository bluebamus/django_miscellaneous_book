from ..models_ex.models_signals_basic import UserProfile

# process with views_signals_basic.py and apps.py

def log_request(sender, **kwargs):
    print('New Request!')


def log_request_adv(sender, environ, **kwargs):
    method = environ['REQUEST_METHOD']
    host = environ['HTTP_HOST']
    path = environ['PATH_INFO']
    query = environ['QUERY_STRING']
    query = '?' + query if query else ''
    print('New Request -> {method} {host}{path}{query}'.format(
        method=method,
        host=host,
        path=path,
        query=query,
    ))


def save_or_create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.user_profile.save()

'''
마지막으로 신호가 동기식이거나 차단된다는 점을 이해하는 것이 중요합니다.
Finally, it is important to understand that signals are synchronous or blocking.

즉, 신호가 트리거된 후 코드를 계속하려면 모든 신호 처리기가 실행을 완료해야 합니다.
This means that all signal handlers will have to finish executing 
before the code can continue after a signal has been triggered.

request_started 신호에 연결된 10개의 신호 처리기가 있는 경우 
Django가 요청의 미들웨어 부분을 실행하기 전에 10개의 모든 처리기가 완료되어야 합니다.

신호를 사용할 때 이것을 염두에 두고 너무 많이 사용하거나 너무 많이 사용하지 마십시오.
'''

# Django는 자체 신호를 생성하고 트리거할 수도 있습니다.
# This can be especially useful when creating a reusable package 
# and you want developers down the road to be able to hook in bit of functionality 
# to your existing code in a proven way.

# In order to create a new signal 
# it is as simple as instantiating a new Signal instance 
# and telling it what additional arguments you will be providing handlers.

import django.dispatch

# ! 해당 라인의 동작은 잘 이해가 안감 추가 학습이 요구됨

todo_complete = django.dispatch.Signal(providing_args=['basic_skills'])