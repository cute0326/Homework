#coding:utf-8
from selenium import webdriver
from time import sleep
import unittest
from datetime import datetime
from bottle import template
import webbrowser

# from html.parser import HTMLParser   提取html内容的
# template在创建html的时候，不支持<>和& 遇到就转码，导致html显示不正确。难道遇到innerHTML就只能静态的写html文件，不能动态生成了码？
#用bottle方法创建动态html文件的方法如下：
# html标记中的变量用双{}包含住
# 若有python代码，则以%开头。
#之后在template函数中给出template_demo 及 其中的参数即可构建html代码。然后创建html文件即可。
# f.write(html_document.encode('GB2312'))   #utf-8汉字也是乱码，GB2312 test是正常的。
#document.body.innerHTML 设置body>…/body>之间的HTML代码  用javascript包含起来

class ZhihuHot(unittest.TestCase):

    def setUp(self):
        self.dr =  webdriver.Firefox()


    def test_read_total_hots(self):
        self.dr.get('https://www.zhihu.com/topic/19607535/top-answers')

        div = self.dr.find_element_by_css_selector('.feed-main>.content')

        title = (div.find_element_by_css_selector('a').text)
        # print(title)

        # display_element = div.find_element_by_css_selector('.zh-summary.summary.clearfix>a').click()
        # sleep(3)
        #参考乙醇的QQ daily hot 抓取的HTML应该外面套着一个div才能正常显示，而不是把div扔掉，只要div里面的内容。
        HTML = self.dr.find_element_by_css_selector('.zm-item-rich-text.expandable.js-collapse-body>.content').get_attribute('innerHTML')

        HTML = self.correct_html(HTML)

        today_time = datetime.now().strftime('%Y%m%d')

        document_name = today_time + '_zhihu_total_hot.html'

        # self.login_blog('admin','211282')
        # self.write_article_blog(title,HTML)

        self.create_html_mannual(document_name,title,HTML)

    def read_today_hots(self):
        self.dr.get('https://www.zhihu.com/topic/19607535/hot')

        div = self.dr.find_element_by_css_selector('.feed-main>.feed-content')

        title = (div.find_element_by_css_selector('a').text)
        # print(title)

        # display_element = div.find_element_by_css_selector('.zh-summary.summary.clearfix>a').click()
        # sleep(3)
        #参考乙醇的QQ daily hot 抓取的HTML应该外面套着一个div才能正常显示，而不是把div扔掉，只要div里面的内容。
        HTML = self.dr.find_element_by_css_selector('.zm-item-rich-text.expandable.js-collapse-body>.content').get_attribute('innerHTML')

        HTML = self.correct_html(HTML)
        today_time = datetime.now().strftime('%Y%m%d')
        # print(today_time)
        document_name = today_time + '_zhihu_today_hot.html'
        # print(document_name)

        # self.login_blog('admin','211282')
        # self.write_article_blog(title,HTML)


        # self.create_html_mannual(document_name,title,HTML)

    # 抓取的HTML中含有转码，需要转换回来。
    def correct_html(self,input_html):
        out_html = input_html.replace('&amp;','&')  #&被转了两次，首先将这个转一下
        out_html = out_html.replace('&nbsp;',' ')
        out_html = out_html.replace('&lt;','<')
        out_html = out_html.replace('&gt;','>')
        out_html = out_html.replace('&amp;','&')
        out_html = out_html.replace('&quot;','"')
        # print(out_html)
        return out_html

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
        # print(content)
        self.dr.get('http://localhost/wordpress/wp-admin/post-new.php')

        self.dr.find_element_by_css_selector('#title-prompt-text').send_keys(title)

        js = 'document.getElementById("content_ifr").contentWindow.document.body.innerHTML=\'%s\'' %(content)

        # js = 'console(' + 'hello world' + ')'
        self.dr.execute_script(js)
         #这个程序中运行javascript就没有报不正常的结尾，所以 infoq那个应该是innerHTML获取的有问题。但是这个确图片不能正常显示

        sleep(20)
        self.dr.find_element_by_css_selector('#publish').click()
        print('OK')

    # 只能硬写，用bottle template自动生成的时候，body中加innerHTML<>和& 总是被转义，还没想到解决的办法。
    def create_html_mannual(self,document_name, title, HTML):
        f = open('..\\' + document_name, 'w+')
        f.write('''<html>
    <head>
      <meta http-equiv="content-type" content="text/html;charset=GB2312" />
      <title>''')
        f.write(document_name)
        f.write('''</title>
    </head>
    <body>''')
        f.write('''<h1>''')
        f.write(title)
        f.write('''</h1>''')
        f.write(HTML)
        f.write('''</body>
  </html>''')

      # 使用浏览器打开html
        webbrowser.open('..\\'+document_name)


    def tearDown(self):
        self.dr.quit()
        # pass

if __name__ == '__main__':
    unittest.main()
