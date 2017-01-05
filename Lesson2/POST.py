# coding:utf-8
import csv
from selenium import webdriver
from time import sleep

class login_blog():
    def __init__(self,driver):
        self.dr = driver

    def login(self,username,password):
        self.dr.get('http://localhost/wordpress/wp-login.php')
        self.dr.find_element_by_id('user_login').clear()
        self.dr.find_element_by_id('user_login').send_keys(username)
        self.dr.find_element_by_id('user_pass').clear()
        self.dr.find_element_by_id('user_pass').send_keys(password)
        self.dr.find_element_by_id('wp-submit').click()
        sleep(3)   #登录怎么也登录不进去，找元素也找不到了，弄了半天，原来是firefox反应慢，需要加一个sleep才行。

    def post_in(self,title,content):
        self.dr.get('http://localhost/wordpress/wp-admin/post-new.php')
        self.dr.find_element_by_id('title').send_keys(title)
        js = 'document.getElementById("content_ifr").contentWindow.document.body.innerHTML = \'%s\'' %content
        print(js)
        self.dr.execute_script(js)
        self.dr.find_element_by_id('publish').click()

if __name__ == '__main__':
    dr = webdriver.Firefox()
    user = 'admin'
    password = '211282'
    test = login_blog(dr)
    test.login(user,password)

    data = csv.reader(open('homework.csv','r'))
    for user in data:
        title = user[0].split(':')[1]
        content = user[1].split(':')[1]
        test.post_in(title,content)

    dr.quit()

