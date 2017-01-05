# coding:utf-8
from selenium import webdriver
import unittest
import random
from selenium.webdriver.support.select import Select
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

class NewUserPost(unittest.TestCase):
    ''' 1. admin log in
        2. create a new author user
        3. admin logout
        4. log in as the new user
        5. post a article
        6. log out
        7. admin log in
        8. add a commend to the new article, then quit
    '''

    def setUp(self):
        # print('set up the NewUserPost')
        self.dr = webdriver.Firefox()

    def generate_random_string(self):
        DIGIT = random.randint(5,10)
        basic_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        string = random.sample(basic_set,DIGIT)
        string = ''.join(string)
        return string

    def test_create_user_and_create_post(self):
        #除了测试类的测试目标加test，其余不带test都是为test服务的。
        self.login_as_admin()
        # user,password = self.create_author_user()
        # self.logout()
        # self.login(user,password)
        post_id = self.post_article_and_return_id()
        self.delete_new_article(post_id)
        self.logout()
        # self.login_as_admin()
        # comment = self.add_comment_on_first_page()
        # sleep(3)   #发布评论之后，直接获取评论不成功，因为评论还没有刷新出来。
        # # print(self.by_css('.comment-content.comment').text)
        # self.assertEqual(self.by_css('.comment-content.comment>p').text,comment)


    def create_author_user(self):
        user = self.generate_random_string()
        email = user + '@qq.com'
        password = self.generate_random_string()

        self.dr.get('http://localhost/wordpress/wp-admin/user-new.php')
        sleep(3)
        self.by_css('#user_login').send_keys(user)
        self.by_css('#email').send_keys(email)
        self.by_css('#pass1').send_keys(password)
        self.by_css('#pass2').send_keys(password)

        Select(self.by_css('#role')).select_by_value('author')
        self.by_css('#createusersub').click()

        return(user,password)

    def post_article(self):
        title = self.generate_random_string()
        content = self.generate_random_string()
        self.dr.get('http://localhost/wordpress/wp-admin/post-new.php')

        self.by_css('#title').send_keys(title)
        self.set_content_by_js(content)
        self.by_css('#publish').click()

    def delete_new_article(self,post_id):
        self.dr.get('http://localhost/wordpress/wp-admin/edit.php')
        row_id = 'post-' + post_id
        print(row_id)
        print(self.dr.current_url)
        sleep(10)
        row = self.dr.find_element_by_id(row_id)
        ActionChains(self.dr).move_to_element(row).perform()
        row.find_element_by_css_selector('.trash').click()
        # row.find_element_by_link_text('移至回收站').click()



    def post_article_and_return_id(self):
        self.post_article()
        sleep(5)
        return(self.by_css('#sample-permalink').text.split('=')[-1])

    def set_content_by_js(self,content):
        js = "document.getElementById('content_ifr').contentWindow.document.body.innerText = '%s'" %content
        self.dr.execute_script(js)
        return content

    def add_comment_on_first_page(self):
        comment = self.generate_random_string()
        self.dr.get('http://localhost/wordpress/')
        url = self.by_css('.entry-title>a').click()
        # url = self.by_css('.entry-title').click()
        # sleep(3)
        # print(self.dr.current_url) #乙醇上课讲可以直接点击'.entry-title，验证了一下不行，必须点击>a才能跳转。
        sleep(3)
        self.by_css('#comment').send_keys(comment)
        self.by_css('#submit').click()

        return comment

    def delete_all_articles(self):
        self.dr.get('http://localhost/wordpress/wp-admin/edit.php')
        self.by_css('#cb-select-all-1').click()
        Select(self.by_css('[name = "action"]')).select_by_value('trash')
        self.by_css('#doaction').click()

    def restore_all_articles(self):
        self.dr.get('http://localhost/wordpress/wp-admin/edit.php')
        self.by_css('.trash').click()      #选择回收站之后，需要反应一下才能把回收站的东西列出来。
        sleep(3)       #不等待几秒，则回收站的东西还没有查询出结果，好多按钮也就没有显示出来。
        #试过等待1秒，即使刷新够快的情况下，按钮是刷新出来了，也可以找到，但是在全选文章的时候，文章列表还是空的。
        self.by_css('#cb-select-all-1').click()
        Select(self.by_css('[name = "action"]')).select_by_value('untrash')
        self.by_css('#doaction').click()

    def login_as_admin(self):
        user = 'admin'
        password = '211282'
        self.login(user,password)

    def login(self, user, password):
        self.dr.get('http://localhost/wordpress/wp-login.php')
        self.by_css('#user_login').clear()
        self.by_css('#user_login').send_keys(user)
        self.by_css('#user_pass').clear()
        self.by_css('#user_pass').send_keys(password)
        self.by_css('#wp-submit').click()
        sleep(3)

    def logout(self):
        url = self.by_css('#wpadminbar').find_element_by_link_text(u'登出').get_attribute('href')
        # self.by_css('#wpadminbar').find_element_by_link_text(u'登出')    No.1
        # print('hello world')   No.2
        #登出等都是不可见元素，所以不能对其执行诸如click, send_keys等动作型操作，但是可以取他的href
        #已经测试过我的这个观点了,执行No.1和No.2组合，就不会报找不到不可见元素的错误，还会打印hello world
        self.dr.get(url)
        # self.by_tag('a')

    def by_css(self,css):
        return self.dr.find_element_by_css_selector(css)

    def by_link_text(self,text):
        return self.dr.find_element_by_link_text(text)

    def by_tag(self,tag):
        return self.dr.find_element_by_tag_name(tag)

    def by_id(self,iid):
        return self.dr.find_element_by_id(iid)

    def tearDown(self):
        # sleep(3)
        # self.dr.quit()
        pass

if __name__ == '__main__':
    unittest.main()
