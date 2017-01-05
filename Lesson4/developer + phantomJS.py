from selenium import webdriver
from time import sleep
import unittest
import sqlite3

class PhantomJS(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.PhantomJS(executable_path = 'D:\phantomjs\\bin\phantomjs.exe')
        #就跟用firefox是一样的，就是换了一个浏览器（无头），然后刚开始用的时候居然只写了路径，没有写.exe文件，真是服了我自己了。

    # def test_read_top(self):
    def test_read_top(self):

        self.dr.get('https://toutiao.io/')
        posts = self.dr.find_elements_by_css_selector('.posts>.post')
        # print(posts)

        count = 0

        self.create_database_and_table('developer.db', 'developer')

        for post in posts:
            count = count + 1
            title_element = post.find_element_by_css_selector('.content>.title')
            title = title_element.text
            # print(author)
            link_element = title_element.find_element_by_css_selector('a')
            link  = link_element.get_attribute('href')
            # print(link)

            self.insert_table('developer.db','developer', count, title, link)

        self.select_table('developer.db','developer')

    def create_database_and_table(self, database, table_name):
        conn = sqlite3.connect('.\\' + database)
        # conn = sqlite3.connect('..\developer.db')  #test证实，在创建数据库的时候，貌似sqlite3的根目录是在py文件的父目录那个级别啊。
        # print('create database successfully!')
        #若表格不存在则创建表格。这样运行时就不会报错了。
        create_sql = 'CREATE TABLE IF NOT EXISTS '+ table_name+ '(id integer primary key, author text, link text)'  #table_name所在的位置直接需要一个字符串，并且table_name就是一个字符串，所以可以直接链接。
        # print(create_sql)
        conn.execute(create_sql)
        # print('create table successfully!')
        conn.close()

    def insert_table(self,database,tablename, value1, value2, value3):
        Insert_SQL = 'INSERT INTO %s VALUES(%d,\"%s\",\"%s\");' %(tablename,value1,value2,value3)

        conn = sqlite3.connect('.\\%s' %(database))
        cu = conn.cursor()
        cu.execute(Insert_SQL)
        conn.commit()
        conn.close()
    def select_table(self,database,tablename):
        conn = sqlite3.connect('.\\%s' %(database))
        select_sql = 'select * from %s;' %(tablename)
        cu = conn.cursor()

        cu.execute(select_sql)
        conn.commit()

        print(cu.fetchall())
        conn.close()

    def by_css(self,css):
        return self.dr.find_element_by_css_selector(css)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
