from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest


"""
测试原则：
1. 不要测试常量，如测试HTML页面tag
"""
class HomePageTest(TestCase):
    # def test_root_url_resolves_to_home_page_view(self):
        # resolve用于解析url，并将其映射到相应的视图函数。检查解析网站根路径”/"时，是否能找到名为home_page的函数
        # found = resolve('/')
        # self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # 测试方法1： 原生测试方法
        # 创建一个HttpRequest对象
        # request = HttpRequest()
        # # 将HttpRequest对象传递给home_page()视图函数，返回response对象
        # response = home_page(request)
        # html = response.content.decode('utf8')
        #
        # self.assertTrue(html.startswith('<!DOCTYPE html>'))
        # self.assertIn('<title>To-Do lists</title>', html)
        # self.assertTrue(html.endswith('</html>'))

        # 测试方法2： 使用Django提供的测试客户端(Test Client)来检查使用那个模板，不用在自己生成HttpRequest
        response = self.client.get('/')

        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))

        self.assertTemplateUsed(response, 'home.html')

