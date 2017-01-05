__author__ = 'Cute'
# atom的当前路径有点诡异：与当前文件的父目录同级（而非与当前目录同级。）pycharm则和当前文件在同一级。
#sqlite3 创建表格时，插入的时候也可以不用游标，但是在查找的时候就需要了。在对表格进行处理时，需要commit才能提交对表格的处理动作。

from selenium import webdriver
import unittest
from time import sleep
import sqlite3
import os

class Developer(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.Firefox()

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
        # Insert_SQL = 'INSERT INTO '+tablename+' VALUES(%d, ' %(value1) +'\"%s\"' %(value2)+',\"%s\" '%(value3)+');'
        Insert_SQL = 'INSERT INTO %s VALUES(%d,\"%s\",\"%s\");' %(tablename,value1,value2,value3)
        #value1的位置需要一个整数，value2,value3的位置需要一个带引号的字符串. 所以需要占位符。
        # print(Insert_SQL)
        conn = sqlite3.connect('.\\%s' %(database))
        cu = conn.cursor()
        cu.execute(Insert_SQL)
        conn.commit()    #别忘了这步。  建表和查询不需要commit，添加，修改，删除都需要commit
        conn.close()
    def select_table(self,database,tablename):
        conn = sqlite3.connect('.\\%s' %(database))
        select_sql = 'select * from %s;' %(tablename)
        cu = conn.cursor()
        # print(select_sql)

        cu.execute(select_sql)
        conn.commit()
        # cu.fetchall()
        print(cu.fetchall())
        conn.close()

    def by_css(self,css):
        return self.dr.find_element_by_css_selector(css)

    def tearDown(self):
        #python删除指定文件的方法。
        # filename = 'D:\Homework\developer.db'
        # os.remove(filename)
        self.dr.quit()
        # pass

if __name__ == '__main__':
    unittest.main()
