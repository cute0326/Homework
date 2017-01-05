from selenium import webdriver
from time import sleep
import unittest
import sqlite3
import os
from bottle import template
import webbrowser

#bottle 利用传入的list 创建 动态html的方法
#zip函数的创建临时组合list的方法。
# 有时候直接指出用什么格式来写template_demo到html文件中会报错，那就创建文本文件，不写编码方式就通过了。
# template 模板对innerHTML的形式不支持，遇到<>就自动转码。
#webbrowser 自动打开文件的方法
# 转到成exe  ---  pip install pyintaller , cmd 切换到py的路径下执行：pyinstaller -F xxx.py 在dist文件夹下就可以找到exe了。小心杀毒软件误杀。

class PhantomJS(unittest.TestCase):

    def  setUp(self):
        input('If you want to see the developer topics, press any key to continue: ')
        self.dr = webdriver.PhantomJS(executable_path = 'D:\phantomjs\\bin\phantomjs.exe')
        #就跟用firefox是一样的，就是换了一个浏览器（无头），然后刚开始用的时候居然只写了路径，没有写.exe文件，真是服了我自己了。

    # def test_read_top(self):
    def test_read_top(self):

        self.dr.get('https://toutiao.io/')
        posts = self.dr.find_elements_by_css_selector('.posts>.post')
        # print(posts)

        count = 0

        links = []
        titles = []
        for post in posts:
            count = count + 1
            title_element = post.find_element_by_css_selector('.content>.title')
            title = title_element.text
            title = str(count) + ': ' + title
            # print(author)
            link_element = title_element.find_element_by_css_selector('a')
            link  = link_element.get_attribute('href')
            # print(link)
            titles.append(title)
            links.append(link)

        self.create_html(titles,links)

    def create_html(self, titles, links):
        template_demo = """
        <html>
        <head><h1>Today's links</h1></head>
        <title>hots link web</title>

        % for title, link in zip(demo_titles,demo_links):
        <body>
           <a href={{link}}>{{title}}</a>
           <br><br>
        </body>
        % end
        </html>
        """
        html_document = template(template_demo, demo_titles = titles,demo_links = links)

        filename = '..\\today\'s developer topic.html'
        # if os.path.exists(filename):
        #     os.remove(filename)

        # w 格式打开的时候，就能保证之前有的话，删除掉了。
        with open(filename, 'wb+') as f:
            f.write(html_document.encode('GB2312'))

        webbrowser.open(filename)

    def by_css(self,css):
        return self.dr.find_element_by_css_selector(css)

    def tearDown(self):
        self.dr.quit()
        # pass

if __name__ == '__main__':
    unittest.main()
