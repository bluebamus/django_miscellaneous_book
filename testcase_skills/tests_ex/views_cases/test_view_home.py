from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse

from testcase_skills.views_ex.tdd_with_python_views import home_page

# reference : https://wikidocs.net/11059

'''
@ TDD 절차는 다음 4단계를 끊임 없이 반복하는 것이다.

1. 기능 테스트
2. 단위 테스트
3. 단위 테스트 및 구현 코딩
4. 리팩토링

@ 어디까지 테스트해야할지 결정하는 것은 쉬운 문제가 아니다.

- 최소한 주요 로직을 검증하는 테스트는 모두 작성한다.
- 최대로 구현하는 시간의 2배 이상은 쓰지 않는다.

@ 좋은 테스트란?

- 한 번에 하나만 테스트한다.
- 실패가 명확해야 한다.
- 빠르게 테스트할 수 있어야 한다.
- 중복된 테스트를 작성하지 않는다.
- 독립적이어야 한다. (다른 테스트이 영향을 받지 않는다.)
- 자동화해야 한다.
'''

class HomePageTest(TestCase):
    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/testcaseskills/home/')
    #     self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>일정관리</title>', html)
        #self.assertTrue(html.endswith('</html>'))
        self.assertTrue(html.strip().endswith('</html>'))

    # 단순히 HTML 문서 내용의 비교라면 render_to_string 함수를 이용할 수도 있다.
    def test_home_page_returns_correct_html_compare(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        expected_html = render_to_string('testcase_skills/home.html')
        self.assertEqual(html, expected_html)

    # Django Test Client 사용
    # assertTemplateUsed() 메소드는 파이썬 표준 모듈 unittest에서 제공하는 게 아니라 Django에서 제공하는 것이다. 
    # 응답을 렌더링하는데 쓰인 템플릿을 확인해준다. 
    # 그런데 Django Test Client로 불러온 응답일 경우에만 동작하는 것에 주의한다.

    # def test_home_page_returns_correct_html_with_test_cliend(self):
        
    #     # debug tool bar의 djdt namespace를 못찾는다는 에러가 발생됨.
    #     # SHOW_TOOLBBAR_CALLBACK 이슈로 정의
    #     # https://github.com/jazzband/django-debug-toolbar/issues/1035
        
    #     response = self.client.get(reverse('testcase_skills:testcase_home'))

    #     html = response.content.decode('utf8')
    #     self.assertTrue(html.startswith('<html>'))
    #     self.assertIn('<title>일정관리</title>', html)
    #     self.assertTrue(html.strip().endswith('</html>'))

    #     self.assertTemplateUsed(response, 'testcase_skills/home.html')

