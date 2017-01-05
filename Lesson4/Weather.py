#coding:utf-8
from selenium import webdriver
import unittest
from time import sleep

class Weather(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.Firefox()

    def read_local_weather(self):   #直接读取默认的天气预报
        self.dr.get('http://www.weather.com.cn/')
        top_div  = self.dr.find_element_by_css_selector('#topTemp')
        top_number = top_div.find_elements_by_css_selector('text')[1].text
        print(top_number)

        low_div = self.dr.find_element_by_css_selector('#lowTemp')
        low_number = low_div.find_elements_by_css_selector('text')[1].text
        print(low_number)

        weather = self.dr.find_element_by_css_selector('#cloud1').text
        print(weather)

    def test_read_Beijing_weather(self):
        self.dr.get('http://www.weather.com.cn/')
        self.dr.find_element_by_id('txtZip').clear()
        self.dr.find_element_by_id('txtZip').send_keys('北京')
        self.dr.find_element_by_css_selector('#btnZip').click()
        sleep(6)
        # print(self.dr.current_url)

        seven_div = self.dr.find_element_by_css_selector('.hover')
        seven_div.click()
        sleep(6)
        seven_days  = self.dr.find_element_by_css_selector('.t.clearfix')
        tomorrow = seven_days.find_elements_by_css_selector('li')[1]
        tomorrow_weather = tomorrow.find_element_by_css_selector('.wea').text
        print(tomorrow_weather)
        tomorrow_temp = tomorrow.find_element_by_css_selector('.tem').text
        # print(tomorrow_temp)
        high_temp = tomorrow_temp.split('/')[0]
        low_temp = tomorrow_temp.split('/')[1].strip()
        print(high_temp + '\n' + low_temp)

        low_temp = int(low_temp.replace('℃', ''))
        high_temp = int(high_temp.replace('℃', ''))

        tomorrow_weather = '今天有雨'

        if('雨' in tomorrow_weather):
            print('请带伞')
            self.send_mail('带伞')

        if (low_temp < 10):
            self.send_mail('保暖')

        if(high_temp > 30):
            self.send_mail('防晒')


    def send_mail(self, content):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
