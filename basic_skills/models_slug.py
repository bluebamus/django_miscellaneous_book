from django.db import models
from django.utils.text import slugify # 쉼표, black를 대쉬(-)로 변경해서 글자들을 연결해줌


# allow_unicode=True 영문을 제외한 다른 언어도 사용할 수 있도록 합니다. => 한글지원
# db_index=True 해당 필드를 인덱스 열로 지정합니다.
# index_together = [['id', 'slug']] 'id'와 'slug'필드를 묶어서 색인하는 '멀티 컬럼 색인'을 지원합니다.

class MyModel(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=201, db_index=True, unique=True, allow_unicode=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug']]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.headline) # 자동생성
        super().save(*args, **kwargs)


'''
urls.py에서 사용 법

from django.urls import path

from . import views

urlpatterns = [
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
'''
