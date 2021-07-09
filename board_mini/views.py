from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Article, User

#==============================Blog FBV 구현==============================

def hello(request, to):
    return HttpResponse('Hello {}.'.format(to))


def list_article(request):                          # 목록보기
    return HttpResponse('list')


def detail_article(request, article_id):            # 상세보기, 상세보기할 article의 id 필요
    return HttpResponse('detail {}'.format(article_id))


def create_or_update_article(request, article_id):
    if article_id: # 수정하기
        if request.method == 'GET':
            return HttpResponse('update {}'.format(article_id))
        elif request.method == 'POST':
            return do_create_article(request)
        else:
            return HttpResponseNotAllowed(['GET', 'POST'])
            # HttpResponse 와 유사 하지만 405 상태 코드를 사용합니다. 
            # 생성자에 대한 첫 번째 인수는 허용 된 메소드 목록 (예 : ['GET', 'POST'] )입니다.
            # 허용되지 않는 메소드로 요청했다는 의미
    else:          # 생성하기
        if request.method == 'GET':
            return HttpResponse('create')
        elif request.method == 'POST':
            return do_update_article(request)
        else:
            return HttpResponseNotAllowed(['GET', 'POST'])


def do_create_article(request):
    return HttpResponse(request.POST)


def do_update_article(request):
    return HttpResponse(request.POST)

#==============================Blog CBV 구현 [TemplateView] ==============================

# *[QuerySet관련 mixin]*

# 다른 제네릭뷰에서는 SingleObjectMixin, MultipleObjectMixin 등을 상속받아 정의가 되어 있습니다. 

# [SingleObjectMixin]
# model = None # 뷰에서 사용할 모델
# queryset = None # 검색 객체
# slug_field = 'slug' # 모델에 정의된 슬러그 필드 이름
# context_object_name = None # 템플릿에 전달될 검색 데이터 이름
# slug_url_kwarg = 'slug' # path 함수로부터 전달받을 슬러그의 키워드 이름
# pk_url_kwarg = 'pk' # path 함수로부터 전달받을 pk의 키워드 이름
# query_pk_and_slug = False # 슬러그와 pk를 데이터 검색에서 사용할 지 여부

# [MultipleObjectMixin]
# allow_empty = True # 검색결과가 없어도 되는 지 여부
# queryset = None # 검색 객체
# model = None # 뷰에서 사용할 모델
# paginate_by = None # 검색데이터가 많을 때 한 페이지당 보여줄 데이터 수량
# paginate_orphans = 0 # 마지막 페이지의 최소 데이터 수량
# context_object_name = None # 템플릿에 전달된 검색 데이터 이름
# paginator_class = django.core.paginator.Paginator # 페이지화를 작동시킬 구현체
# page_kwarg = 'page' # 검색할 페이지 번호에 대한 키워드 이름
# ordering = None # 검색시 사용할 정렬방식. ORM의 order_by

#====================================================================================

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib import messages

# 모델을 기반으로 하는 ListView나 DetailView등은 클래스 변수 model을 정의할 경우 
# 자동으로 모델명(소문자) + '_list.html' 또는 '_detail.html'로 템플릿파일을 자동으로 생성합니다. 
# 파일명을 이런식으로 작명한다면 나중에 더 복잡한 제네릭뷰를 사용할 때 편리하고 오류를 줄일 수 있습니다

class ArticleListView(TemplateView):         # 게시글 목록
    template_name = 'board_mini/article_list.html'
    queryset = Article.objects.all()         # 모든 게시글

    def get(self, request, *args, **kwargs):
        ctx = {
            #'view': self.__class__.__name__, # 클래스의 이름, 해당 제네릭뷰 인스턴스의 클래스 이름
            #'data': self.get_queryset()            # 검색 결과
            #'articles': self.queryset
            # 이렇게 호출하면 갱신된 DB 데이터가 아니라 캐시된 데이터를 전달함, 새로 추가된 데이터는
            # print 등으로 인한 DB 평가가 되지 않으면 출력되지 않음, order_by하면 평가가 되는듯
            'articles': self.queryset.order_by('-id')
        }
        return self.render_to_response(ctx) # render_to_response 템플릿을 자동적으로 기본 템플릿 엔진을 이용해서 html로 변환해주는 함수

    def get_queryset(self):
        if not self.queryset:
            self.queryset = Article.objects.all()
        return self.queryset

class ArticleDetailView(TemplateView):
    template_name = 'board_mini/article_detail.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'                 # 검색데이터의 primary key를 전달받을 이름, <pk>로 변환해서 사용해도 무관함

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset     # queryset 파라미터 초기화
        pk = self.kwargs.get(self.pk_url_kwargs) # pk는 모델에서 정의된 pk값, 즉 모델의 id
        article = queryset.filter(pk=pk).first()    # pk로 검색된 데이터가 있다면 그 중 첫번째 데이터 없다면 None 반환

        if not article:
            raise Http404('invalid pk')
        return article
        
    def get(self, request, *args, **kwargs):
        article = self.get_object()
        
        ctx = {
            'article': article
        }
        return self.render_to_response(ctx)

#@method_decorator(csrf_exempt, name='dispatch')   # 테스트를 위해 CSRF verification 예외처리
class ArticleCreateUpdateView(TemplateView):
    template_name = 'board_mini/article_update.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'
    create_success_message = '게시글이 저장되었습니다.'
    update_success_message = '게시글이 업데이트되었습니다.'

    # kwargs에 pk가 있다는 것은 update를 의미하고, pk가 없다는 건 create를 의미합니다.
    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        article = queryset.filter(pk=pk).first()
        
        if pk and not article:                    # 검색결과가 없으면 곧바로 에러 발생
            raise Http404('invalid pk')
        return article

    def get(self, request, *args, **kwargs):
        article = self.get_object()

        ctx = {
            'article': article
        }
        return self.render_to_response(ctx)


    # http post의 경우 request.body 객체에 데이터 내용이 문자열 형태로 전달됩니다. 
    # 이 데이터가 딕셔너리로 변환이 가능할 경우 장고의 미들웨어가 자동으로 request.POST 객체에 변환된 값을 저장합니다. 
    # 변환된 값은 딕셔너리와 동일하게 읽을 수 있습니다. 하지만 immutable 객체이기 때문에 수정이 불가합니다.


    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')           # request.POST 객체에서 데이터 얻기
        post_data = {key: request.POST.get(key) for key in ('title', 'content', 'author')}
        for key in post_data:                         # 세가지 데이터 모두 있어야 통과
            if not post_data[key]:
                messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tags='danger') # error 레벨로 메시지 저장

        # messsages 모듈의 debug, info, success, warning, error 5가지 함수 중 하나를 선택해서
        # request 객체와 저장할 메시지를 전달하면 됩니다

        # messages.get_messages(request) 함수는 현재까지 저장된 메시지들을 반환합니다. 
        # 커스텀 레벨과 extra_tags은 장고 문서에서 확인하자!
        # 저장된 메시지들이 1개 이상이라면 현재의 코드에서는 반드시 오류가 발생했다는 것이기 때문에 
        # 액션로직을 실행하지 않도록 했습니다. 
        # article 변수는 액션로직 안에서 정의하기 때문에 만약 오류가 발생하면 
        # action이 'update'인 경우 article을 검색해오고 'create'인 경우는 None을 저장하도록 했습니다. 
            # 코드에서 상위 부분을 찾지 못함 None을 어디에 저장할까?
        # if ~ else 문법을 이용해서 3항 연산자처럼 표현한 식을 익혀두시면 유용하게 사용하실 수 있습니다.

        if len(messages.get_messages(request)) == 0:                  # 메시지가 있다면 아무것도 처리하지 않음
            if action == 'create':
                article = Article.objects.create(**post_data)
                messages.success(self.request, self.create_success_message)  # success 레벨로 메시지 저장
            elif action == 'update':
                article = self.get_object()
                for key, value in post_data.items():
                    setattr(article, key, value)
                article.save()
                messages.success(self.request, self.update_success_message)  # success 레벨로 메시지 저장
            else:
                messages.error(self.request, '알 수 없는 요청입니다.', extra_tags='danger')     # error 레벨로 메시지 저장

            return HttpResponseRedirect('/boardmini/article/') # 정상적인 저장이 완료되면 '/articles/'로 이동됨
    
        ctx = {
            'article': self.get_object() if action == 'update' else None
        }
        return self.render_to_response(ctx)           # 액션 작업 후 화면을 보냄


#==============================Auth CBV 구현 [CreateView,]==============================

from django.contrib.auth import get_user_model
from django.views.generic import CreateView

from .forms import UserRegistrationForm

# model 이 정의되면 내부적으로 Form 객체를 자동 생성하는데 
# 이 때 모델의 모든 필드를 이용해서 폼을 만드는 것이 아니라 
# fields 라는 클래스변수를 참조해서 정의되어 있는 필드만 이용합니다.

# 자동으로 해당 앱의 templates 디렉토리에서 앱이름의 디렉토리 하위의 모델명_form.html 파일을 템플릿으로 사용합니다. 
# 우리의 예제에서는 user/template/user/user_model.html 파일을 검색하게 되는 겁니다.

# template_suffix 클래스변수를 정의하면 template 파일명의 _form 대신에 다른 문자열로 대치도 가능합니다. 
# 예를들어 template_suffix 를 '_registration' 으로 변경하면 
# user/template/user/user_registration.html 파일을 찾게 되는 것이죠.

class UserRegistrationView(CreateView):
    model = User                            # 자동생성 폼에서 사용할 모델
    #fields = ('email', 'username', 'password')  # 자동생성 폼에서 사용할 필드
    form_class = UserRegistrationForm
    success_url = '/boardmini/article/' # 해당 변수가 없으면 get_absolute_url을 접근함