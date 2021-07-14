from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from board_mini.models import Article


# 생성한 앱에 맞는 sitemap 클래스를 생성해줍니다.
# 저는 posts라는 앱과 products라는 앱을 생성하였고, 
# 이때 각 models.py에서 Ardexpost, Product 라고 클래스를 정의하였습니다. 

# 예시로 Products 앱을 등록하는 걸로 하고 진행해보겠습니다. 
# (위에 제반설정에 말씀드린 것과 같이 Products 앱에는 url 정의를 받아오는 reverse 함수를 사용하여 작성하였습니다.)

# class ProductSitemap(Sitemap):
#     def items(self):
#         return Product.objects.all()


# 만약 어플리케이션을 만들지 않고 단일 html 파일을 만들고 static 파일에 저장하신 경우, 
# static sites 역시 등록이 가능합니다. 
# 
# 예시로 'about-us'라는 사이트를 만들었다고 가정합니다.

# class StaticViewSitemap(Sitemap):
#     def items(self):
#         return ['about-us']
        
#     def location(self, item):
#         return reverse(item)



# 참고 : https://pythonblog.co.kr/blog/46/

# from myapp.blog.models import PyBlog

# class PytonBlogSitemap(Sitemap):
#     changefreq = 'weekly'
#     priority = 0.7

#     def items(self):
#         results = PyBlog.objects.all().order_by('-regist_dt')       
#         return results

#     def location(self, obj):
#         return """/blog/%s""" % obj.pk

#     def lastmod(self, obj):
#         return obj.update_dt



# 메인 화면, 마이페이지의 장바구니, 고객센터 세 페이지를 사이트맵에 추가한다고 가정하겠습니다.

# priority는 해당 클래스의 우선 순위를 나타냅니다. 0~1사이 값을 지정하게 되는데,
# 다른 클래스를 여러 개 더 추가하여 사이트맵에 추가할 경우 어떤 것을 (상대적으로) 우선하여 
# 구글에게 제공할 지를 결정합니다.

# changefreq는 검색엔진에 대한 해당 내용이 얼마나 자주 바뀌는 지를 알려주지만, 
# 이거를 'always'로 지정한다고 해서 검색 엔진이 지정된 주기로 무조건 인덱싱하도록 결정하는 것은 아닙니다. 
# 따라서 그냥 상대적인 정보를 주는 부분이며 강력하게 작동한다고 보기는 힘들겠네요.

class BoardMiniSitemap(Sitemap): 
    priority = 0.5 
    changefreq = 'weekly' 
    
    def items(self): 
        return Article.objects.all().order_by('-created_at')  

    def location(self, obj):
        return """/board_mini/%s""" % obj.pk

    def lastmod(self, obj):
        return obj.created_at


# ! xml 접근 및 출력은 되지만 sitemap 정보는 출력이 안됨 테스트가 더 필요함

