from selenium import webdriver
import unittest
from time import sleep

class PM25(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.Firefox()

    def test_order_PM(self):
    # def order_PM(self):
        content = []
        BeijingPM = self.Read_Beijing()
        content.append(('Beijing',BeijingPM))
        ShanghaiPM = self.Read_Shanghai()
        content.append(('Shanghai',ShanghaiPM))
        GuangzhouPM = self.Read_Guangzhou()
        content.append(('Guangzhou',GuangzhouPM))
        ShenzhenPM = self.Read_Shenzhen()
        content.append(('Shenzhen',ShenzhenPM))

        result_content = sorted(content, key=lambda item:item[1], reverse = False)
        print(result_content)

        self.write_PM_txt(result_content)

    def Read_Shenzhen(self):
        self.dr.get('http://www.pm25.com/shenzhen.html')

        return int(self.dr.find_element_by_css_selector('.bi_aqiarea_num').text)

    def Read_Beijing(self):
        self.dr.get('http://www.pm25.com/beijing.html')
        return int(self.dr.find_element_by_css_selector('.bi_aqiarea_num').text)

    def Read_Shanghai(self):
        self.dr.get('http://www.pm25.com/shanghai.html')
        # return self.dr.find_element_by_css_selector('.bi_aqiarea_num').text
        return int(self.dr.find_element_by_css_selector('.bi_aqiarea_num').text)

    def Read_Guangzhou(self):
        self.dr.get('http://www.pm25.com/guangzhou.html')
        # return self.dr.find_element_by_css_selector('.bi_aqiarea_num').text
        return int(self.dr.find_element_by_css_selector('.bi_aqiarea_num').text)

    def write_PM_txt(self,contents):
        f = open('..\PMresult.txt','w+')
        for content in contents:
            f.write(content[0] + ',' + str(content[1]))
            f.write('\n')
        f.close()

    def write_PM_csv(self,contents):
        f = open('..\PMresult.csv','w+')
        for content in contents:
            f.write(content[0] + ',' + str(content[1]))
            f.write('\n')
        f.close()

    def tearDown(self):
        self.dr.quit()

if __name__ == '__main__':
    unittest.main()
