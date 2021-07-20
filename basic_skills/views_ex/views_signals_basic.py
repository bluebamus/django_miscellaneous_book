

# 참고 : https://django-advanced-training.readthedocs.io/en/latest/features/signals/#signals

'''
@ Some of the most common built-in signals in Django are:

django.db.models.signals.pre_save and django.db.models.signals.post_save 
- These signals are triggered before or after a model instance save method is called.

django.db.models.signals.pre_delete and django.db.models.signals.post_delete 
- These signals are triggered before or after a model instance's delete method is called 
  and before or after a queryset's delete method is called.

django.core.signals.request_started and django.core.signals.request_finished 
- These signals are triggered when Django starts or finishes an HTTP request.

django.contrib.auth.signals.user_logged_in and django.contrib.auth.signals.user_logged_out 
- These signals are triggered after a user successfully logs in or out of the application.
'''

# django.db.models.signals.post_save 신호는 특정 모델을 저장할 때 수행해야 하는 작업을 연결하는 데 유용합니다.

'''
예를 들어, 우리의 할일 애플리케이션에 시스템에서 생성된 모든 사용자에 대해 
생성되었는지 확인하려는 사용자 프로필 모델(UserProfile)이 있다고 가정합니다. 

이를 수행하는 한 가지 방법은 django.contrib.auth의 사용자 모델에
post_save 신호 핸들러를 연결하는 것입니다.
'''

'''
신호 모듈에는 Django가 제공하는 핵심 신호인 
request_started, request_finished, got_request_exception, setting_changed가 있습니다. 

이것은 자신의 신호를 생성하기 위해 수행해야 하는 작업에 대해 좋은 예시들을 제공합니다.

signal reference code = https://github.com/django/django/blob/main/django/core/signals.py

dispatcher reference code = https://github.com/django/django/blob/main/django/dispatch/dispatcher.py

* 실재 signal에 대한 모든 구현은 dispatch에 있음

signal class는 django.dispatch.dispatcher 에서 찾을 수 있으며 django.dispatch 에서 가져올 수 있습니다.

'''

# from django.dispatch import Signal

# request_started = Signal(providing_args=["environ"])


'''
* connect()

1. receivers에 대해 lookup_key가 생성됨 : 
    - 이를 통해 신호는 개별 receiver를 식별하고 동일한 receiver가 signal에 두 번 이상 연결되지 않도록 보장해줌
        하나의 수신기는 하나의 signal만 연결됨
2. self.lock는 context manager를 이용하여 signal을 잠근다. 
-    receiver가 self.receiver list에 한번에 오직 하나의 process에 의해서만 수정, 추가되는 것이 보장될 수 있도록 해줌
3. lock context manager block 내부에 수신자 리스트에 중복해서 추가되지 않도록 보장하기 위해 lookup_key를
    기반으로 확인하고 아직 없는 경우 최종적으로 추가한다.
4. reciver가 signal receiver list에 추가되었다.
    - 이 list는 send 메서드에서 사용된다.
'''

#==================================================================================================

'''
* send()

def send(self, sender, **named):

def send_robust(self, sender, **named):


1. send 메서드는 첫 번째 요소(element)가 receiver 함수형, 두번째 요소(element)가 
   receiver를 호출에 대한 응답(response)인 튜플 list를 반환합니다.
    - signal은 내부 메서드로 _live_receivers를 가지고 있습니다. 
    - _live_receivers는 명시(지정)된 발신자의 active receivers list를 반환합니다.
2. 구현은 1번 과정을 simple list comprehension(반복 가능한 객체)로 수행함.
3. * signal을 trigger하기 위해 send 메소를 호출 하는데 있어 한가지 이슈가 있다.
    - 만약 하나의 receivers가 예외를 발생하면 모든 receiver가 실행한다는 것을 보장할 수 없다는 것이다.
    - 이 문제에 있어 send_robust가 도움을 줄 수 있다.
4. send_robust 메소드는 예외가 포착되어 추후 평가를 위해 반환값(return value)에 추가된다는 점을 제외하고 
   send 메소드와 동일한 작업을 수행합니다.
    - 이 방법은 모든 수신자가 실행될 수 있도록 보장해줍니다.
5. send 메소드가 simple list comprehension(반복 가능한 객체)를 가지고 있는 경우, 
   send_robust 메소드는 발생된 예외 결과 혹은 receiver의 호출, 둘 중 하나가 응답 리스트에 추가되었거나
   호출된게 있는지, try-except를 이용해 receiver를 확인하는 for loop를 가지고 있다.
6. 내부적으로 Django는 오직 signal을 보내기 위해서 send 메소드를 사용하며, 
   send_robust는 사용자 정의 signal들을 위해서 사용된다.
'''

#==================================================================================================

'''
* request_started 및 request_finished는 어디에서 호출될까?

class HttpResponseBase:
    ...
    def close(self):
        ...
        signals.request_finished.send(sender=self._handler_class)


1. 우리는 request_started 및 request_finished signal이 어디에서 생성되는지 알고 있지만(django.core.signals)
   해당 signal들이 triggered(전송) 되는 위치는 어디일까?
    - Django는 django.core.handlers.wsgi.WSGIHandler __call__ 메서드에서 request_started 신호를 보냅니다.
    - __call__ 메서드의 2행에서 보내는 호출을 볼 수 있습니다.
        - wsgi reference code : https://github.com/django/django/blob/main/django/core/handlers/wsgi.py#L135
    - WSGIHandler 클래스는 Django 애플리케이션의 주요 진입점입니다.
    - 인스턴스가 인스턴스화되면 __call__ 메서드가 각 요청에 대해 호출됩니다.
    - request_started 신호는 기본적으로 각 요청에서 가장 먼저 호출되는 신호입니다.

2. Django는 django.http.response.HttpResponseBase 클래스 닫기 메서드에서 request_finished 신호를 보냅니다.
        - http response reference code : https://github.com/django/django/blob/main/django/http/response.py#L27 
    - close 메소드는 응답 중 WSGI server에 의해 호출됩니다. 이때, request_finished signal이 전송됩니다.
        - http response reference code : https://github.com/django/django/blob/main/django/http/response.py#L238

3. 중요한 부분으로 close가 하는 가장 마지막 작업은 request_finished 신호를 보내는 것입니다.
'''

#==================================================================================================

'''
* django.dispatch.dispatcher.Signal의 for-else block에 대한 부연 설명

1. 해당 for문은 일반적인 구조가 아니기 때문에 예제를 통해 동작을 이해하고자 함

letters = ['a', 'b', 'c']
looking_for = 'a'

for letter in letters:
    if letter == looking_for:
        print('Found the letter!')
        break
else:
    print("Didn't find the letter.")


    - else block은 전체 for 루프가 완료 되었을때, break 문에 도달하지 않은 경우 실행된다.

'''

#==================================================================================================

'''
* Context manager

1. 많은 경우, 코드에서 리소스를 확보하고자 리소스를 사용하고 나서 정리(청소)를 해야합니다.
    - 이것은 파일(열기, 처리, 닫기), 잠금(잠금, 처리, 해제) 및 기타 많은 리소스로 작업할 때의 경우입니다.
    - 이러한 일은 매우 일반적인 흐름이기 떄문에 파이썬은 이를 훨씬 더 멋지게 만드는 명령문(statement)을 추가했습니다.

# working with files

# the standard method
file = open('tmp.txt')
...  # processing the file
file.close()

# context manager method
with open('tmp.txt') as file:
    ...  # processing the file


2. 위 두 가지 방법은 모두 파이썬에서 잘 동작을 합니다.
    - 하지만 the context manager method(with 문 사용)이 더 안전합니다.
    - 이 컨텍스트의 with 문은 처리 코드에서 예외가 발생하더라도 파일이 닫히도록 보장합니다.
    
3. django.dispatch에서 컨텍스트 관리자의 또 다른 사용을 볼 수 있습니다.
    - dispatcher.Signal classes connect method. 
    - 이곳에서 with 문을 사용하여 잠금을 획득하고 해제합니다.
    - 다시 한 번, with 블록 코드에서 예외가 발생하더라도 잠금이 해제되는 것이 보장되기 때문에 더 안전하다는 이점이 있습니다.
'''

#==================================================================================================

'''
* Hands-on Exercises - 실습

1. todo_done과 todo_undone signals을 구현합니다.
    - mark_done과 mark_undone과 같은 Todo 모델 메서드에서 send method를 호출합니다.
    - 완료되었거나 취소된 항목을 기록하는(logs) 콜백 신호에 연결을 합니다.

2. Possible Solution

# todo/signals.py
import django.dispatch

todo_done = django.dispatch.Signal(providing_args=['item'])
todo_undone = django.dispatch.Signal(providing_args=['item'])


# todo/models.py
...
from .signals import todo_done, todo_undone
...
class Todo(models.Model):
    ...
    def mark_done(self):
        if not self.done:
            self.done = True
            self.save()
            todo_done.send(sender=self.__class__, item=self)

    def mark_undone(self):
        if self.done:
            self.done = False
            self.save()
            todo_undone.send(sender=self.__class__, item=self)
...


# todo/tasks.py
...
def log_todo_action(sender, item, **kwargs):
    if item.done:
        logger.info(f'Item complete: {item.item}')
    else:
        logger.info(f'Item undone: {item.item}')


# todo/app.py
...
from . import signals, tasks
...
class TodoConfig(AppConfig):
    ...
    def ready(self):
        signals.todo_done.connect(tasks.log_todo_action)
        signals.todo_undone.connect(tasks.log_todo_action)       



Django Signals Documentation : https://docs.djangoproject.com/en/3.2/topics/signals/

'''