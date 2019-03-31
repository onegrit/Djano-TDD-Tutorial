from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

from lists.models import Item

"""
测试原则：
1. 不要测试常量，如测试HTML页面tag
2. 一个测试只测试一件事情
3. 确保功能测试之间相互隔离(如何隔离测试：运行功能测试后待办事项一直存在于数据库中，这回影响下次测试的结果）
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

        # self.assertTemplateUsed(response, 'home.html')

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    # def test_only_save_items_when_necessary(self):
    #     self.client.get('/')
    #     self.assertEqual(Item.objects.count(), 0)

    # def test_display_all_list_items(self):
    """该职责由ListViewTest test_display_all_items（） 实现"""
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
    #
    #     response = self.client.get('/')
    #
    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        """测试保存一个新的待办事项"""
        # To-Do: 代码异味：POST请求的测试太长了
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        # POST请求后应该重定向到首页
        # 将下面的测试职责移到新的单元测试中 test_redirects_after_post
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/')
        # self.assertIn('A new list item', response.content.decode())
        # self.assertTemplateUsed(response, 'home.html')

    def test_redirects_after_post(self):
        """测试POST提交后是否重定向到相应页面"""
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):
    def test_display_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertTemplateUsed(response, 'list.html')


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
