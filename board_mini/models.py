from django.db import models
from django.utils import timezone
from django.http import HttpResponseRedirect
from .user_models import UserBasicModel

# reference : https://swarf00.github.io/2018/11/23/build-model.html

# shell test :
# from bbs.models import Article
# from datetime import datetime
# article = Article.objects.create(title='How to create a article', content='1. import Article class\n2. invoke \'create\' method of Article\'s manager.', author='swarf00', created_at='2018-11-22')
# print(article)
# print('{} title: {}, content: {}, author: {} created_at: {}'.format(article.id, article.title, article.content, article.author, article.created_at))
# article.created_at = '2018-11-22 01:15'

# article.refresh_from_db()               # db로 부터 새로 검색
# article.created_at.strftime('%Y-%m-%d')
# article.objects.filter(author='swarf00').first() # author='swarf00'인 첫번째 레코드 검색
# article.objects.filter(author='swarf00').last()  # author='swarf00'인 마지막 레코드 검색
# 

# shell로 테스트시 create 함수는 positional argument도 지원하지만 인자가 여러개이거나 한눈에 보기 어려운 경우 
# keyword arguemnt로 전달하는 것이 보기 좋습니다.

# auto_now_add를 True로 설정하면 create메소드가 호출될 때 항상 현재시간이 기록됩니다

class Article(models.Model):
    title      = models.CharField('제목', max_length=126, null=False)
    content    = models.TextField('내용', null=False)
    author     = models.CharField('작성자', max_length=16, null=False)
    
    #created_at = models.DateTimeField('작성일', auto_now_add=True)
    #created_at.editable = True    # auto_now_add=True로 admin 페이지에서 수정이 불가능하기 때문에 created의 editable 속성에 True를 설정했습니다.

    created_at = models.DateTimeField('작성일', default=timezone.now) 
    # 대신 디폴트값으로 현재시간을 저장하도록 수정하면 자동으로 created_at 값이 생성될 뿐만 아니라 
    # editable 속성도 True 로 설정되기 때문에 일석이조입니다

    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)


class User(UserBasicModel):

    def __str__(self):
        return '[{}] {}'.format(self.email, self.username)