from selenium import webdriver
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
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# assert 'To-Do' in browser.title, "Browser title was " + browser.title
# Alice使用应用的故事
# 应用请就输入一个待办事项
# 爱丽丝在文本矿中输入了"Buy peacock feathers"（购买羽毛球）
# 爱丽丝的爱好是使用假蝇做饵钓鱼
# 她按回车键后，页面更新了
# 待办事项表格中显示了"1: Buy peacock feathers"

# 页面中又显示了一个文本框，可以输入其他的待办事项
# 她输入了"Use peacock feathers to make a fly"
# 爱丽丝做事很有条理

# 页面再次更新，他的待办事项清单中显示了这两个待办事项

# 爱丽丝想知道这个网站是否会记住她的待办事项清单
# 她看到网站为她生成了一个唯一的URL
# 而且页面中有一些文字解说功能

# 她访问那个URL，发现她的待办事项列表还在

# 她很满意，去睡觉了
