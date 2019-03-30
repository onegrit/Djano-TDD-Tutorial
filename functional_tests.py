from selenium import webdriver
from selenium.webdriver.common import keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        """setUp方法在各个测试方法之前运行"""
        # 打开浏览器
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """tearDown方法在各个测试方法之后运行"""
        # 关闭浏览器
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Alice听说有一个很酷的在线待办事项应用
        # 她去看了这个应用的首页
        self.browser.get("http://localhost:8000")

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
        time.sleep(2)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(
        #     any(row.text == '1: Buy peacock feathers' for row in rows),
        #     f"New to-do item did not appear in table. Contents were:\n {table.text}"
        # )
        # 将assertTrue改为assertIn
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        # 页面中又显示了一个文本框，可以输入其他的待办事项

        # 她输入了"Use peacock feathers to make a fly"
        # 爱丽丝做事很有条理，再输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(keys.Keys.ENTER)
        time.sleep(1)
        # 页面再次更新，清单中显示了两个待办事项
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])

        # 爱丽丝想知道这个网站是否会记住她的待办事项清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说功能

        self.fail('Finish the test!!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# assert 'To-Do' in browser.title, "Browser title was " + browser.title
# Alice使用应用的故事


# 页面再次更新，他的待办事项清单中显示了这两个待办事项


# 她访问那个URL，发现她的待办事项列表还在

# 她很满意，去睡觉了
