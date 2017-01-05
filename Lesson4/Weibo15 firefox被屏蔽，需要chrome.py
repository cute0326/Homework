from selenium import webdriver
from time import sleep
import unittest

class WEIBO15(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.Chrome()  #微博拦截firefox浏览器，chrome好了之后，可以用chrome试试。

    def test_top15(self):
        self.dr.get('http://d.weibo.com/100803?cfs=&Pl_Discover_Pt6Rank__5_filter=hothtlist_type%3D1')
        lists = self.dr.find_element_by_css_selector('.pt_ul.clearfix')
        # lists = lists.dr.find_elements_by_css_selector('li')
        # print(lists)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()