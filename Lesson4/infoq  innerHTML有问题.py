__author__ = 'Cute'

# coding:utf-8
from selenium import webdriver
import unittest
from time import sleep
from bottle import template
import webbrowser

# QQ网站抓取出来的innerHTML就可以直接用，不需要再correct一下内容里的innerHTML内容。所以到底要不要correct一下HTML需要把HTML打印出来看下就知道了
# 如果这个HTML正常的话，那用bottle自动生成一下html可以不呢？
class InfoQ(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.Firefox()

    # def test_read_QQ_hots(self):     #QQ头条抓取innerHTML写wordpress正常(含图片，不需要处理innerHTML)
    def read_QQ_hots(self):
        self.dr.get('http://www.qq.com/')
        url = self.dr.find_element_by_css_selector('#todaytop>a').get_attribute('href')
        self.dr.get(url)
        title = self.dr.find_element_by_css_selector('.title').text
        innerHTML = self.dr.find_element_by_css_selector('.article').get_attribute('innerHTML')
        print(innerHTML)

        self.login_blog('admin','211282')
        self.write_article_blog(title,innerHTML)

        # self.create_html_automatically('QQdailyhots.html',title,innerHTML)

    def test_read_test_articles(self):
        self.dr.get('http://www.infoq.com/cn/Testing/articles/')
        articles = self.dr.find_elements_by_css_selector('.news_type2')
        # print(articles)

        for article in articles:
            title = article.find_element_by_css_selector('a').get_attribute('title')
            print(title)
            link = article.find_element_by_css_selector('a').get_attribute('href')
            # print(link)
            self.dr.get(link)
            innerHTML = self.dr.find_element_by_css_selector('.text_info.text_info_article').get_attribute('innerHTML')
            print(innerHTML)
            self.login_blog('admin','211282')

            self.write_article_blog(title, innerHTML)

            break

    def login_blog(self,username,password):
        self.dr.get('http://localhost/wordpress/wp-login.php')
        self.dr.find_element_by_css_selector('#user_login').clear()
        self.dr.find_element_by_css_selector('#user_login').send_keys(username)
        self.dr.find_element_by_css_selector('#user_pass').clear()
        self.dr.find_element_by_css_selector('#user_pass').send_keys(password)
        self.dr.find_element_by_css_selector('#wp-submit').click()
        sleep(3)

    def write_article_blog(self,title, content):
        content = content.strip()
        print(content)
        self.dr.get('http://localhost/wordpress/wp-admin/post-new.php')

        self.dr.find_element_by_css_selector('#title-prompt-text').send_keys(title)

        js = 'document.getElementById("content_ifr").contentWindow.document.body.innerHTML=\'%s\'' %(content)

        self.dr.execute_script(js)

        self.dr.find_element_by_css_selector('#publish').click()

        print('OK')

# QQ innerHTML 用bottle template模板自动生成html也还是不成功。目前还找不到解决方法，还有innerHTML的只能硬写，不能自动生成。
    def create_html_automatically(self,document_name, title, innerHTML):
        template_demo = """
                <html>
                <head><h1>{{demo_title}}</h1></head>
                <title>{{demo_name}}</title>

                <body>
                    {{demo_html}}
                </body>
                % end
                </html>
                """
        html_document = template(template_demo, demo_name = document_name, demo_title=title, demo_html=innerHTML)

        # w 格式打开的时候，就能保证之前有的话，删除掉了。
        with open('..\\'+ document_name, 'w+') as f:
            f.write(html_document)

        webbrowser.open('..\\'+ document_name,)

    def tearDown(self):
        # self.dr.quit()
        pass

if __name__ == "__main__":
    unittest.main()
