from selenium import webdriver
from time import sleep
import unittest

class WEBO10(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.Firefox()


    def test_read_top_10(self):
        self.dr.get('http://d.weibo.com/102803?from=unlogin_home&mod=pindao&type=hotweibo#_rnd1456632403002')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()