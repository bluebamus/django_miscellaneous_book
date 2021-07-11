from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Article, User

#==============================Blog FBV 구현==============================

# reference : https://swarf00.github.io/2018/11/23/setup-project.html


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
        
        # if pk and not article:                    # 검색결과가 없으면 곧바로 에러 발생
        #     raise Http404('invalid pk')
        # return article

        if pk:
          if not article:
            raise Http404('invalid pk')
          elif article.author != self.request.user:                             # 작성자가 수정하려는 사용자와 다른 경우
            raise Http404('invalid user')
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

        #post_data = {key: request.POST.get(key) for key in ('title', 'content', 'author')}
        post_data = {key: request.POST.get(key) for key in ('title', 'content')} # 작성자를 입력받지 않도록 수정

        for key in post_data:                         # 세가지 데이터 모두 있어야 통과
            if not post_data[key]:
                messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tags='danger') # error 레벨로 메시지 저장

        post_data['author'] = self.request.user                                  # 작성자를 현재 사용자로 설정
        
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


#==============================Auth register, resend email CBV 구현 [CreateView,FormView ]==============================

from django.contrib.auth import get_user_model
from django.views.generic import CreateView, FormView
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .forms import UserRegistrationForm, VerificationEmailForm
from .mixins import VerifyEmailMixin

# model 이 정의되면 내부적으로 Form 객체를 자동 생성하는데 
# 이 때 모델의 모든 필드를 이용해서 폼을 만드는 것이 아니라 
# fields 라는 클래스변수를 참조해서 정의되어 있는 필드만 이용합니다.

# 자동으로 해당 앱의 templates 디렉토리에서 앱이름의 디렉토리 하위의 모델명_form.html 파일을 템플릿으로 사용합니다. 
# 우리의 예제에서는 user/template/user/user_model.html 파일을 검색하게 되는 겁니다.

# template_suffix 클래스변수를 정의하면 template 파일명의 _form 대신에 다른 문자열로 대치도 가능합니다. 
# 예를들어 template_suffix 를 '_registration' 으로 변경하면 
# user/template/user/user_registration.html 파일을 찾게 되는 것이죠.

#============ 리팩토링 => VerifyEmailMixin

# class UserRegistrationView(CreateView):
#     #model = User                            # 자동생성 폼에서 사용할 모델
#     model = get_user_model()
#     #fields = ('email', 'username', 'password')  # 자동생성 폼에서 사용할 필드
#     form_class = UserRegistrationForm
#     verify_url = '/boardmini/user/verify/'
#     success_url = '/boardmini/article/' # 해당 변수가 없으면 get_absolute_url을 접근함
#     email_template_name = 'user/email/registration_verification.html'

#     '''
#     default_token_generator 는 사용자 데이터를 가지고 해시데이터를 만들어주는 객체인데 
#     이것을 이용해서 생성된 사용자 고유의 토큰을 생성합니다. 
    
#     생성된 토큰과 사용자id(pk) 값을 인증페이지의 url에 포함하여 어떤 사용자의 토큰인지 
#     url만 보고 확인할 수 있도록 합니다.
#     '''

#     token_generator = default_token_generator

#     '''
#     UserRegistrationForm 는 ModelForm 을 상속받은 클래스인데 
#     form_valid 메소드를 호출하면 데이터베이스에 저장(Form.save())을 하고 
#     저장된 데이터를 폼객체의 instance 변수에 저장을 합니다. 
    
#     그래서 token 을 생성할 때 이 form.instance 를 이용하도록 했습니다. 
#     (장고의 내장 뷰에서는 폼클래스에서 save() 메소드 호출 직후 처리를 하기도 합니다.)
#     '''
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         if form.instance:
#             self.send_verification_email(form.instance)
#         return response

#     def send_verification_email(self, user):
#         token = self.token_generator.make_token(user)
#         url = self.build_verification_link(user, token)
#         subject = '회원가입을 축하드립니다.'
#         message = '다음 주소로 이동하셔서 인증하세요. {}'.format(url)
#         html_message = render(self.request, self.email_template_name, {'url': url}).content.decode('utf-8')
#         user.email_user(subject, message, settings.EMAIL_HOST_USER, html_message=html_message)
#         messages.info(self.request, '회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.')


#     def build_verification_link(self, user, token):
#         return '{}/user/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)

'''
ender 함수는 HttpResponse 객체를 반환합니다. 
HttpResponse 객체의 content 속성에 렌더링된 메시지가 저장되어 있는데 http로 전송할 수 있도록 
byte 로 인코딩되어 있습니다. 

email_user 메소드에 전달할 때 반드시 utf-8 로 디코딩을 해줘야 합니다. 
email_user 메소드를 호출할 때 기존의 텍스트 메시지와 html 메시지 둘다 전달한 이유는 
일부 이메일 클라이언트에서는 html 형식의 이메일을 지원하지 않을 수 있어서 
html 메시지를 보여줄 수 없는 이메일 클라이언트에게 기본적으로 보여줄 내용으로 텍스트 메시지를 전달하는 것이 좋습니다.

django.template.loader.render_to_string 함수를 이용하면 곧바로 렌더링된 utf-8 문자열을 출력합니다.
'''

'''
* gmail 설정 에서 보안 수준이 낮은 앱 허용 을 활성해야함
reference : https://support.google.com/accounts/answer/185833?hl=ko

mansger.py shell로 send_email 테스트 방법

1. from django.conf import settings
2. from board_mini.models import User
3. from django.core.mail import send_mail
4. user = User.objects.get(email='redbamus@gmail.com')
5. send_mail('test', 'this is a test',settings.EMAIL_HOST_USER,[user.email])

'''

class UserRegistrationView(VerifyEmailMixin, CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = '/boardmini/user/login/'
    verify_url = '/boardmini/user/verify/'

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # form_valid 메소드를 호출하면 데이터베이스에 저장(Form.save())을 하고 
        # 저장된 데이터를 폼객체의 instance 변수에 저장을 합니다
        # send_verification_email에서 user 변수로 사용
        
        if form.instance:
            self.send_verification_email(form.instance)
        return response

#============ 리팩토링 => VerifyEmailMixin

# class ResendVerifyEmailView(FormView):
#     model = get_user_model()
#     form_class = VerificationEmailForm
#     success_url = '/boardmini/user/login/'
#     template_name = '/boardmini/user/resend_verify_email.html'
#     email_template_name = '/boardmini/user/email/registration_verification.html'
#     token_generator = default_token_generator

#     def send_verification_email(self, user):
#         token = self.token_generator.make_token(user)
#         url = self.build_verification_link(user, token)
#         subject = '회원가입을 축하드립니다.'
#         message = '다음 주소로 이동하셔서 인증하세요. {}'.format(url)
#         html_message = render(self.request, self.email_template_name, {'url': url}).content.decode('utf-8')
#         user.email_user(subject, message, from_email=settings.EMAIL_HOST_USER, html_message=html_message)
#         messages.info(self.request, '회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.')
    
      # request.META는 사용자의 IP 주소와 사용자 Agent(일반적으로 웹 브라우저의 이름과 버전)를 포함해 
      # 지정된 요청에 대해 사용할 수 있는 모든 HTTP 헤더가 들어있는 파이썬 딕셔너리다.
#     def build_verification_link(self, user, token):
#         return '{}/user/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)

#     def form_valid(self, form):
#         email = form.cleaned_data['email']
#         try:
#             user = self.model.objects.get(email=email)
#         except self.model.DoesNotExist:
#             messages.error(self.request, '알 수 없는 사용자 입니다.')
#         else:
#             self.send_verification_email(user)
#         return super().form_valid(form)


class ResendVerifyEmailView(VerifyEmailMixin, FormView):
    model = get_user_model()
    form_class = VerificationEmailForm
    success_url = '/boardmini/user/login/'
    template_name = 'board_mini/resend_verify_email.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, '알 수 없는 사용자 입니다.')
        else:
            # ???
            # modelform은 instance를 썼는데 여기는 왜 user를 사용했을까?
            # form은 form_valid에 instance를 전달하지 않는 것일까?
            # 상식적으로 말이 안되기 떄문에, 확인이 필요하지만 form에서도 instance를 사용 가능할 것이다.
            self.send_verification_email(user)
        return super().form_valid(form)

#==============================Auth 메일 인증 페이지 생성 CBV 구현 [,]==============================

'''
인증이메일의 링크를 클릭했을 때 이동할 인증페이지를 만들어야 합니다. 
먼저 인증뷰를 생성합니다. 
인증뷰는 url의 사용자id 값과 token 을 가지고 해당 사용자의 정상적인 token 값인지 확인 후 
정상적인 경우 로그인페이지(또는 웰컴페이지)로 이동시키고 인증이 완료되었다는 메시지를 출력시켜주면 됩니다. 

정상적이지 않은 경우 인증실패 메시지와 인증메일을 재발송할 수 있도록 링크를 추가하면 됩니다. 
어차피 나중에 로그인 페이지에서 인증이메일 재발송 기능을 추가할 예정이니 인증실패시 
로그인페이지로 이동할 수 있는 링크를 제공해주도록 하겠습니다.
'''

'''
토큰의 유효성 확인도 default_token_generator 를 이용합니다. 
유효한 토큰일 경우 사용자의 is_active 를 True 로 변경시키고 저장해야 합니다. 
주의할 것은 인증에 실패했다고 is_active 를 False 로 변경시키면 안됩니다. 

혹시나 악의적인 목적으로 url 을 난수로 대입할 경우 정상적인 사용자id와 충돌이 생겨 인증상태가 변경될 수도 있으니 
인증이 실패할 경우는 그대로 무시하고, 다만 실패되었다는 메시지만 출력해주는 것으로 확인시켜주면 됩니다.

인증이 성공할 경우 곧바로 인증세션정보를 생성해서(django.contrib.auth.login()) 로그인된 것으로 처리한다면 
사용자 입장에서는 좀 편리할 수 있으나 그만큼 보안강도가 약해지는 것이기 때문에 
별도로 로그인을 하도록 유도하는 것이 보안에 좀 더 좋은 방법입니다.
'''

# 인증이메일의 링크를 클릭했을 때 이동할 인증페이지
class UserVerificationView(TemplateView):

    model = get_user_model()
    redirect_url = 'boardmini/user/login/'
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.error(request, '인증이 실패되었습니다.')
        return HttpResponseRedirect(self.redirect_url)   # 인증 성공여부와 상관없이 무조건 로그인 페이지로 이동

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.objects.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()     # 데이터가 변경되면 반드시 save() 메소드 호출
        return is_valid


#==============================Auth login CBV 구현 [LoginView,]==============================

from django.contrib.auth.views import LoginView
from .forms import LoginForm

# LoginView 는 뷰만 와 폼만 제공해주고, 템플릿은 제공해주지 않습니다. 
# 기본값으로 registraion/login.html 로 설정되어 있는데 실제 찾아보면 존재하지 않는 파일입니다. 

# form_vaild 함수에서 auth_login 함수 실행 후 self.get_success_url() 메소드가 리턴하는 주소로 이동하는데 
# 이때 self.get_success_url() 메소드는 3가지의 값들을 순서대로 검색하며 가장 먼저 검색된 값을 반환합니다. 
#  아무런 설정을 하지 않으면 LOGIN_REDIRECT_URL 에 정의된 '/accounts/profile/' 로 반환하게 됩니다.

# login redirection url 검색 순서
## 1. 요청된 폼의 필드 중 next라는 이름을 가진 필드의 값. 빈 값인 경우 2번으로 패스
## 2. url의 query parameter 중 next 라는 이름을 가진 값. 빈 값인 경우 3번으로 패스
## 3. 설정파일에 설정된 LOGIN_REDIRECT_URL 변수로 설정된 값. (기본값: '/accounts/profile/')

# login redirection url 설정 방법
## 1. form에 next라는 이름의 hidden 필드를 추가하고 '/article/' 값을 기본으로 세팅한다.
## 2. form의 action 속성에 '/user/login/?next=/article/' 이라는 값을 세팅한다.
## 3. 설정 파일에 LOGIN_REDIRECT_URL = '/article/' 이라고 설정한다.
## 4. one more thing! get_success_url() 메소드를 오버라이드 해서 '/article/' 문자열을 반환한다.

'''
 이 네가지 방법은 각각 사용해야 할 가장 좋은 케이스들이 있습니다. 
 누가 정해놓은 건 아니지만 장고로 개발된 대개의 서비스가 그렇게 사용하고 있다는 겁니다. 
 다시 4가지의 케이스를 나열해 볼테니 각각의 케이스가 몇번의 방법을 사용해야 좋을 지 생각을 해보세요.

로그인 이후 redirection url 결정을 고려해야 할 케이스

1. 대부분의 경우 사용자가 로그인 후 아무런 조건이 없을 때 이동할 페이지. 기본적인 REDIRECT URL

2. 다양한 방식의 로그인을 제공해서 로그인 이후 이동할 페이지가 단순한 규칙으로 다를 경우. 
예) 모바일과 PC 버전의 화면들을 각각 제공하며 url의 path에 따라 화면이 결정될 경우 
/m/user/login/ => /m/article/, /user/login => /article/ 또는 다국어를 지원해서 언어별로 path를 구분하는 경우 
/ko/user/login => /ko/article/, /en/user/login => /en/article/ 

3. 로그인하기 전에는 redirect url을 알 수 없을 경우.
예) 로그인한 사용자의 권한레벨에 따라 슈퍼유저인 경우 
admin 사이트로, staff 권한인 경우 대시보드 화면으로 이동, 로그인한 사용자의 연령이 20세 미만일 경우 특정화면으로 이동

4. 어떤 화면으로 이동하려 했으나 인증된 사용자만 접근이 허락된 화면이어서 자동으로 로그인화면으로 이동한 경우 
예) 로그인 하지 않은 사용자가 /admin/user/user/ 를 접근했으나 강제로 로그인 화면으로 이동되고, 
로그인된 이후에 원래 사용자가 접근하려 했던 /admin/user/user/ 로 되돌려 보내야 하는 경우

각 케이스별로 한 가지만 선택해야 하는 경우
1 => 3번 방법
2 => 2번 방법
3 => 4번의 get_success_url 메소드를 케이스 별 처리하도록 오버라이딩
4 => 2번 방법

선호하는 방법은 3, 2, 1, 4 순서

* get_success_url 메소드 오버라이딩)은 
장고에서 기본적으로 제공하는 루틴을 무시하고 재정의 하는 것이니 코드의 일관성을 해치는 방법

3번 방법(설정파일에 LOGIN_REDIRECT_URL 변수 설정)은 무조건 설정하세요. 
그리고 예외적인 케이스는 전부 2번 방법(url에 query 파라미터 추가)으로 처리합니다. 
만일 2번 방법보다 1번의 방법이 코드가 효율적이거나 url로 redirect url이 노출되는 것이 싫은 경우에만 
1번을 사용합니다.

'''

# settings.py에 auth 관련 설정 변수
## LOGIN_URL = "/boardmini/user/login/"
## LOGIN_REDIRECT_URL = "/boardmini/article/"
## AUTH_USER_MODEL = 'board_mini.User'

'''
새로 생성된 LoginForm을 UserLoginView 에 설정해주면 되는데, 
LoginView 처럼 form_class 클래스변수에 정의해서 오버라이드 하는 방법도 있으나 
권장하는 방법은 authentication_form 이라는 클래스변수에 LoginForm을 설정하는 것 입니다. 

강제사항은 아니나 LoginForm 내부적으로 authentication_form 을 먼저 확인하고 없으면 
form_class를 이용하도록 되어 있습니다. 

즉 커스터마이징 할 거라면 authentication_form 를 사용하라는 원 제작자의 의도가 있습니다. 
'''

'''
세션 백엔드 모듈이름    |	기능
django.contrib.sessions.backends.db     |	데이터베이스에 저장하는 백엔드
django.contrib.sessions.backends.cache  |	캐시에 저장하는 백엔드
django.contrib.sessions.backends.cache_db   |	캐시와 데이터베이스를 병행하는 백엔드
django.contrib.sessions.backends.file   |	파일에 저장하는 백엔드
django.contrib.sessions.backends.signed_cookie  |	쿠키에 저장하는 백엔드

강력한 방법으로 매 요청 때마다 request.session 객체의 cycle_key() 메소드를 호출하는 겁니다. 
cycle_key() 메소드가 호출될 때마다 sessionid 가 변경되고 변경된 값이 쿠키에 저장이 됩니다. 
sessionid 가 노출되었더라도 sessionid 를 악의적인 목적으로 사용하기 전에 또다른 요청을 한다면 
이전의 sessionid 값은 유효하지 않은 것이 됩니다. 
하지만 매 요청마다 세션 백엔드가 sessionid 를 다시 저장해야 하기 때문에 
서버의 가용성이 조금 떨어진다는 것이 문제입니다. 
서버의 성능보다는 안정성이 중요하다면 이 방법을 사용해도 좋습니다.

사용자 모델을 매번 불러오는 것이 아니라 미들웨어는 일단 SimpleLazyObject 객체를 반환합니다. 
request.user = SimpleLazyObject(lambda: get_user(request)) request.user 가 가리키는 SimpleLazyObject 객체는 
처음에는 빈 객체이지만 request.user 객체에서 특정 속성(is_authenticated, is_superuser, is_staff 등)을 접근할 때 
실제 데이터를 불러와 캐싱합니다. 

즉 request.user 객체의 속성값을 읽으려 하기 전까지는 장고(인증 미들웨어)는 사용자가 누구인지 모르고 
세션객체의 내용만 알 수 있습니다. 
이렇게 설계된 이유는 모든 요청 때마다 사용자 정보를 불러온다면 
사용하지도 않을 사용자 정보 때문에 서버 자원을 소모하지 않게 하기 위함입니다. 
SimpleLazyObject 는 인증 외의 많은 부분에서도 유용하게 사용할 수 있으니 사용법을 반드시 기억해주시길 바랍니다

장고에서 기본적으로 세션객체에 _auth_user_id, _auth_user_backend, _auth_user_hash 
이 세가지 정보를 딕셔너리 형태로 저장합니다.

key     |	데이터
_auth_user_id   |	사용자 정보 id
_auth_user_backend  |	로그인할 때 사용한 인증 백엔드
_auth_user_hash |	사용자정보 테이블에 저장된 패스워드값의 해시값

로그인 할 때 이메일과 비밀번호를 입력하는데 http에서는 입력한 문자(이메일, 비밀번호 등) 
그대로 네트워크를 통해 전송이 됩니다. 
잘 알려진대로 공용 네트워크에서는 동일한 네트워크 안에 있는 누군가에게 해당 내용이 노출이 될 여지가 많이 있습니다. 
그래서 어떠한 안전한 인증 기능을 제공하기 이전에 반드시 https를 제공해야 합니다. 
할 수만 있다면 https를 반드시 사용하시기 바랍니다.
https를 제공할 수 없다면 소셜로그인 기능을 연동하는 것도 좋은 방법입니다

인증된 사용자에게만 접속을 허용하기 뷰클래스에 LoginRequiredMixin 이 추가(CBV)되었거나 
핸들러 함수가 login_required 데코레이터로 wrapping 을 합니다. 
이것들은 내부적으로 requests.user.is_authenticated 값을 비교합니다.
여러분들도 별도의 프로세스로 사용자의 인증여부를 확인해야 하는 경우 
가급적 requests.user.is_authenticated 의 값을 이용하시면 오류의 가능성이 현저히 줄어듭니다.
'''

'''
장고의 auth 프레임워크에서 제공하는 뷰들이 어떻게 구현되어 있는 지 살펴보시면 새로운 뷰 개발에 도움이 되실 겁니다.

django.contrib.auth.views.PasswordResetView
django.contrib.auth.views.PasswordResetDoneView
django.contrib.auth.views.PasswordResetConfirmView
django.contrib.auth.views.PasswordResetCompleteView
django.contrib.auth.views.PasswordChangeView
django.contrib.auth.views.PasswordChangeDoneView
'''

class UserLoginView(LoginView):           # 로그인
    authentication_form = LoginForm
    template_name = 'board_mini/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)    