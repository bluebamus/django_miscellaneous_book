from django.contrib import admin
  
from .models import Article, User

# @admin.register(Article) == 코드 제일 하단에 admin.site.register(Article, ArticleAdmin) 처럼 사용해도 동일한 결과
# reference : https://darrengwon.tistory.com/348

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'date_created')  # date_created는 아래 정의한 메소드
    list_display_links = ('id', 'title')                      # 상세페이지로 이동할 수 있는 필드 리스트

    def date_created(self, obj):                              # create_at 필드의 출력형식을 변경해주는 메소드
        return obj.created_at.strftime("%Y-%m-%d")

    date_created.admin_order_field = 'created_at'             # date_created 컬럼 제목을 클릭시 실제 어떤 데이터를 기준으로 정렬할 지 결정
    date_created.short_description = '작성일'                   # date_created 컬럼 제목에 보일 텍스트


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'joined_at', 'last_login_at', 'is_superuser', 'is_active')
    list_display_links = ('id', 'email')
    exclude = ('password',)                           # 사용자 상세 정보에서 비밀번호 필드를 노출하지 않음

    def joined_at(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")

    def last_login_at(self, obj):
        if not obj.last_login:
            return ''
        return obj.last_login.strftime("%Y-%m-%d %H:%M")

    joined_at.admin_order_field = '-date_joined'      # 가장 최근에 가입한 사람부터 리스팅
    joined_at.short_description = '가입일'
    last_login_at.admin_order_field = 'last_login_at'
    last_login_at.short_description = '최근로그인'