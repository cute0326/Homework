from selenium import webdriver
from time import sleep
import time
import unittest
import random

#结论，在前台测试的话，需要refresh一下，来确认前后台沟通正常。refresh
# webdriver读不出隐藏元素

class Smile_Task(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.Firefox()
        self.dr.get('http://localhost:12306/')

    # def test_create_task(self):
    def create_task(self):
        # self.dr.get('http://localhost:8080/')

        # 防止点击到其他的按钮，可能有些隐藏按钮什么的。

        self.dr.find_element_by_css_selector('#app .btn-primary').click()

        sleep(2)

        input_title  = 'to do %s' %(time.time())
        input_des = 'desc %s' %(time.time())
        self.dr.find_element_by_css_selector('#title').send_keys(input_title)
        self.dr.find_element_by_css_selector('#desc').send_keys(input_des)
        #直接写.btn-primary的话，因为创建按钮也是.btn-primary，所以，会点击到后面那个创建的按钮上去，而不是前面这个对话框中的创建任务按钮。
        self.dr.find_element_by_css_selector('.modal-footer>.btn-primary').click()


        sleep(2)
        #其实也不是因为视频中所说的缓存，是因为selenium读的太快了，只要sleep一下也是可以读到正确答案的。乙醇视频刚开始讲错了。
        # 但是如果是为了测试前后台是不是通信正常，刷新还是很有必要的。防止前台写好了，后台没通信的问题。

        self.dr.refresh()    #防止前后台没通信
        first_row = self.dr.find_element_by_tag_name('tbody>tr')   # css selector和tag name都可以找到。

        title = first_row.find_elements_by_tag_name('td')[1].text
        desc = first_row.find_elements_by_tag_name('td')[2].text

        self.assertEqual(input_title, title)
        self.assertEqual(input_des, desc)

    def test_delete_task(self):
    # def delete_task(self):

        # self.dr.get('http://localhost:8080/')
        num, Id = self.get_random_line_ID()

        all_rows = self.dr.find_elements_by_css_selector('tbody>tr')

        all_rows[num].find_element_by_css_selector('.btn-danger').click()
        #等待alert弹出
        sleep(2)
        self.dr.switch_to_alert().accept()

         #等待刷新
        sleep(2)
        left_rows = self.dr.find_elements_by_css_selector('tbody>tr')

        result =  True
        for left_row in left_rows:
            target_id = left_row.find_element_by_css_selector('td').text
            # print('target_id is %s' %target_id)
            if(Id in target_id ):
                print('delete fail!')
                result = False

            self.assertEqual(result, True)

    # def test_finish_task(self):
    def finish_task(self):
        # self.dr.get('http://localhost:8080/')
        #can even find there level element
        # text = self.dr.find_elements_by_css_selector('tbody>tr>td')[-2].text

        # finish之后，在class = done中的td中确认。是不是加了下划线，是不是完成和删除按钮消失了。
        num, Id = self.get_random_line_ID()
        print('the number is %d' %num)
        print('the select record\'s id is %s' %Id)

        finish_row = self.dr.find_elements_by_css_selector('tbody>tr')[num]
        finish_row.find_element_by_css_selector('.btn-success').click()
        sleep(2)

        #查找全部已经完成的项目。
        finish_rows = self.dr.find_elements_by_css_selector('.done')

        result = False
        for row in finish_rows:
            finish_id = row.find_element_by_css_selector('td').text

            #元素隐藏之后，webdrive是读不出来他的内容的。
            if Id == finish_id:
                text = row.text
                # print(text)
                self.assertNotIn('完成' , text)
                self.assertNotIn('删除' , text)
                result = True

        self.assertEqual(result, True)

    def get_random_line_ID(self):

        # select random line in all lines to delete/finish , first get the randsom ID .
        all_rows = self.dr.find_elements_by_css_selector('tbody>tr')
        lines_num = len(all_rows)
        print(lines_num)

        # 任选一行删除
        num = random.randint(0,(lines_num-1))
        # print(num)

        Id = all_rows[num].find_element_by_css_selector('td').text
        # print(Id)

        return (num, Id)

    def tearDown(self):
        # self.dr.quit()
        pass


if __name__ == '__main__':
    unittest.main()
