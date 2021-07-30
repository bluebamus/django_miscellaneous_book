from django.test import TestCase
from django.urls import resolve
from testcase_skills.views_ex.tdd_with_python_views import home_page


class HomePageTest(TestCase):
    # success
    def test_root_url_resolves_to_home_page_view_success(self):
        found = resolve('/testcaseskills/home/')
        self.assertEqual(found.func, home_page)

    # failed
    # def test_root_url_resolves_to_home_page_view_failed(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, home_page)