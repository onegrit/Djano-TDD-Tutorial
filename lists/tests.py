from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

from lists.models import Item, List

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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class ListViewTest(TestCase):
    """
    职责：测试列表视图
    测试内容：
        1. 测试列表是否使用正确的模板
        2. 测试每个列表只包含属于该列表的待办事项
    """

    def test_uses_list_template(self):
        aList = List.objects.create()

        response = self.client.get(f'/lists/{aList.id}/')

        self.assertTemplateUsed(response, 'list.html')

    def test_display_only_items_for_that_list(self):
        """
        测试每个列表只包含属于该列表的待办事项
        :return:
        """
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="other list 1", list=other_list)
        Item.objects.create(text="other list 2", list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, "other list 1")
        self.assertNotContains(response, "other list 2")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertEqual(response.context['list'], correct_list)


class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class NewItemTest(TestCase):
    """向list中添加item"""

    def test_can_save_a_post_request_to_an_existing_list(self):
        """测试:向一个现存list中添加item"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list', 'list_id': f'{correct_list.id}'}
        )
        # 断言：数量，内容
        self.assertEqual(Item.objects.count(), 1)  # 判断添加数据量是否正确
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
