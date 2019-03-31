import os
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import keys
from django.test import LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        """setUp方法在各个测试方法之前运行"""
        # 打开浏览器
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        """tearDown方法在各个测试方法之后运行"""
        # 关闭浏览器
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """不使用time.sleep()显示等待时间，而使用重试循环"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Alice听说有一个很酷的在线待办事项应用
        # 她去看了这个应用的首页
        # self.browser.get("http://localhost:8000")
        self.browser.get(self.live_server_url)

        # 她在网页的标题和头部看到了“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        # self.fail('Finish the test!')
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 应用请就输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # 爱丽丝在文本矿中输入了"Buy peacock feathers"（购买羽毛球）
        # 爱丽丝的爱好是使用假蝇做饵钓鱼
        inputbox.send_keys('Buy peacock feathers')

        # 她按回车键后，页面更新了
        # 待办事项表格中显示了"1: Buy peacock feathers"
        inputbox.send_keys(keys.Keys.ENTER)
        # time.sleep(2)
        # 使用函数，重构下面的代码
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(
        #     any(row.text == '1: Buy peacock feathers' for row in rows),
        #     f"New to-do item did not appear in table. Contents were:\n {table.text}"
        # )
        # 将assertTrue改为assertIn
        # self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        # 页面中又显示了一个文本框，可以输入其他的待办事项

        # 她输入了"Use peacock feathers to make a fly"
        # 爱丽丝做事很有条理，再输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(keys.Keys.ENTER)
        # time.sleep(1)
        # 页面再次更新，清单中显示了两个待办事项
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        # 爱丽丝想知道这个网站是否会记住她的待办事项清单
        # 想让每个都用户都能保存自己的待办事项清单（待办事项列表）
        # 待办事项清单有多个待办事项组成
        # 她看到网站为她生成了一个唯一的URL（每个用户独享一个URL）
        # 而且页面中有一些文字解说功能

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """测试多个用户可以开启不同的待办任务清单列表"""
        # Alice新建一个代办事项清单（列表）
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(keys.Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        # 她注意到清单有唯一的URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # 现在一个叫做弗朗西斯的新用户访问了网站
        ## 我们使用一个新浏览器会话
        ## 确保Alice的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Firefox()
        # 弗朗西斯访问首页
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # 弗朗西斯输入一个新待办事项，新建一个清单
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(keys.Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # 弗朗西斯获得了她的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 这个页面还是没有Alice的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # self.fail('Finish the test!!')

    def test_layout_and_styling(self):
        # Alice访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # 她看到输入框完美的居中显示
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # 她新建了一个清单，看到输入框仍完美地居中显示
        # inputbox.send_keys('testing')
        # inputbox.send_keys(keys.Keys.ENTER)
        # self.wait_for_row_in_list_table('1: testing')
        # inputbox = self.browser.find_element_by_id('id_new_item')
        # self.assertAlmostEqual(
        #     inputbox.location['x'] + inputbox.size['width'] / 2,
        #     512,
        #     delta=10
        # )

    # if __name__ == '__main__':
    #     unittest.main(warnings='ignore')

    # assert 'To-Do' in browser.title, "Browser title was " + browser.title
    # Alice使用应用的故事

    # 页面再次更新，他的待办事项清单中显示了这两个待办事项

    # 她访问那个URL，发现她的待办事项列表还在

    # 她很满意，去睡觉了
