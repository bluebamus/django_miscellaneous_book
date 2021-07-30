from django.test import TestCase
from django.urls import resolve

from testcase_skills.views_ex.tdd_with_python_views import home_page, home_page_post
from testcase_skills.views_ex.tdd_with_post_views import home_page

# reference : https://wikidocs.net/11061

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/testcaseskills/homepostrender/')
        self.assertEqual(found.func, home_page_post)

    def test_uses_home_template(self):
        response = self.client.get('/testcaseskills/homepostrender/')
        self.assertTemplateUsed(response, 'testcase_skills/home_post.html')

    # item_text 변수에 A new list item 문자열 값을 담아 / 경로에 POST 요청한다. 
    # 이 때 POST 요청을 받아 실제 서버에서는 어떠한 처리도 하지 않으므로 
    # 아래와 같은 예상되는 테스트 실패를 확인할 수 있다.

    def test_can_save_a_POST_request(self):
        # response = self.client.post('/testcaseskills/homepost/', data={'item_text': 'A new list item'})
        # self.assertIn('A new list item', response.content.decode())
        response = self.client.post('/testcaseskills/homepostrender/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'testcase_skills/home_post.html')