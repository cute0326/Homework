# coding:utf-8
from time import ctime,sleep
from selenium import webdriver
import random
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import unittest

class Creat_and_Commend(unittest.TestCase):

    def __init__(self):
        self.dr = webdriver.Firefox()

    def generate_string(self):
        DIGIT = random.randint(5,10)
        test = ''.join(random.sample((list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')), DIGIT))
        return test

    def create_new_user(self):  #id menu-users
        # self.find_element_by_css_selector('#menu-users>a.text('用户')').find_element_by_css_selector()
        # 鼠标一步步找元素总是出错，结果乙醇也是直接用的url。。。
        user = self.generate_string()
        email = user + '@qq.com'
        password = self.generate_string()

        self.dr.get('http://localhost/wordpress/wp-admin/user-new.php')
        self.by_css('#user_login').send_keys(user)
        self.by_css('#email').send_keys(email)
        self.by_css('#pass1').send_keys(password)
        self.by_css('#pass2').send_keys(password)
        Select(self.by_css('#role')).select_by_value('author')
        #好奇葩，刚开始wordpress做这个的时候，怎么也选择不上作者，总是按照一个默认选项建立。后来我在网页中选择了几次下拉框，运行就可以选择作者了。难道是这个网页之前那个功能没有用过，所以没有激活。太有意思了
        #这个奇葩的wordpress，害我郁闷了一晚上。结果我想要解决的问题，几乎都没有在老师的课堂中找到结果，人家根本就直接绕过去了。
        #结果我后来重新安装也好用了，不知道怎么回事儿。好奇葩。无论是从select的包中引入，还是ui的包中引入（select中的举例，都没有问题了。）
        self.by_css('#createusersub').click()

        return(user,password)

    def add_commend(self):
        content = self.generate_string()
        self.dr.get('http://localhost/wordpress/')
        print('will click the article')
        sleep(10)
        self.by_css('.entry-title').click()
        print('have click the button')
        self.assertEqual(self.dr.current_url,'http://localhost/wordpress/?p=19')
        sleep(3)
        self.by_css('#comment').send_keys(content)

        return content

    def logout(self):  # wpadminbar
        url = self.by_css('#wpadminbar').find_element_by_link_text('登出').get_attribute('href')
        print(url)
        self.dr.get(url)
        # sleep(3)
        self.dr.find_element_by_tag_name('a').click()


    def login_as_admin(self):
        user = 'admin'
        password = '211282'
        self.login(user,password)

    def login(self,username,password):
        self.dr.get('http://localhost/wordpress/wp-login.php')
        self.dr.find_element_by_id('user_login').clear()
        self.dr.find_element_by_id('user_login').send_keys(username)
        self.dr.find_element_by_id('user_pass').clear()
        self.dr.find_element_by_id('user_pass').send_keys(password)
        self.dr.find_element_by_id('wp-submit').click()
        sleep(3)   #登录怎么也登录不进去，找元素也找不到了，弄了半天，原来是firefox反应慢，需要加一个sleep才行。


    def post_article(self):
        title = self.generate_string()
        content = self.generate_string()
        self.dr.get('http://localhost/wordpress/wp-admin/post-new.php')
        self.dr.find_element_by_id('title').send_keys(title)
        js = 'document.getElementById("content_ifr").contentWindow.document.body.innerHTML = \'%s\'' %content
        print(js)
        self.dr.execute_script(js)
        self.dr.find_element_by_id('publish').click()

    def by_css(self,css):
        return self.dr.find_element_by_css_selector(css)

    def by_id(self,id):
        return self.dr.find_element_by_id(id)

    def by_link(self,element):
        return self.dr.find_element_by_link_text(element)

    def quit(self):
        self.dr.quit()

if __name__ == '__main__':
    test = Creat_and_Commend()
    # test.login_as_admin()
    # user,password = test.create_new_user()
    # test.logout()
    # test.login(user,password)
    # test.post_article()
    # test.logout()
    test.login_as_admin()
    test.add_commend()
    test.logout()
    test.quit()
