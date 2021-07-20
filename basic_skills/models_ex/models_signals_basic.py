from django.db import models
from django.urls import reverse

class UserProfile(models.Model):
    title = models.CharField(max_length=100)
    block_address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    # def get_absolute_url(self):
    #     return reverse("store_detail", kwargs={"pk": self.pk})


# ! 해당 코드의 동작은 잘 이해가 안감 추가 학습이 요구됨

# 아마도 해당 모델 instance를 save하고나서 그 시그널을 특정 app에 전달해서 대기중인 watching status를
# done 혹은 finish, update status로 변경하도록 제어할 수 있는 기능 같은데 좀 더 살펴봐야 함

# Note the call to todo_complete.send. 
# This is calling the send method of the custom signal instance. 
# This setup allows other developers, or yourself in other areas of your code, 
# to hook into the event (signal) of completing a todo item 
# and attach any functionality they would like to that event.

from ..tasks.signal_basic_log_tasks import todo_complete

class Todo(models.Model):
    description = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def mark_complete(self):
        if not self.done:
            self.done = True
            self.save()
            todo_complete.send(sender=self.__class__, todo=self)