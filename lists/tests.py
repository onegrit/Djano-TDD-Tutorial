from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


# Create your tests here.

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        # resolve用于解析url，并将其映射到相应的视图函数。检查解析网站根路径”/"时，是否能找到名为home_page的函数
        found = resolve('/')
        self.assertEqual(found.func, home_page)
