# coding:utf-8
from selenium import webdriver
import unittest
from time import sleep
import csv
# 杩欎釜鍒氬紑濮嬫垜鎯崇殑澶鏉備簡锛岃繕鐐瑰嚮鍒拌櫄骞荤被锛岄潪铏氬够绫婚噷闈㈠幓鎵句簡锛岀粨鏋滈噷闈㈢殑鏍峰紡澶嶆潅鐨勮姝伙拷??
# 鐪嬩簡鐪艰胺甯嗙殑鎵嶅弽搴旇繃鏉ワ紝涓哄暐鎬绘槸鎶婇棶棰樻兂鐨勯偅涔堝鏉傚憿銆傝鐩镐俊鑷繁鐨勬墜涓凡缁忔帉鎻′簡瑙ｅ喅闂鐨勬柟娉曪拷?锟藉彧锟斤拷?瑕佽杞昏交锟斤拷?鐐瑰氨鍙互浜嗭拷??
# sorted的用法需要注意一下，之前用过这个方法，后来忘记了。
class DOUBANDUSHU(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.Firefox()

    def goto_web(self):
        self.dr.get('https://book.douban.com//')
        # print(self.dr.current_url)

    def test_movie_list(self):
        self.goto_web()
        books = self.dr.find_elements_by_css_selector('.list-summary>li')

        content = []
        for book in books:
            book_title = book.find_element_by_css_selector('.title').text
            print(book_title)
            book_rate = book.find_element_by_css_selector('.average-rating').text
            print(book_rate)
            book_author = book.find_element_by_css_selector('.author').text
            print(book_author)
            book_class = book.find_element_by_css_selector('.book-list-classification').text.split('/')[0]
            print(book_class)
            book_review = book.find_element_by_css_selector('.reviews').text
            print(book_review)
            link = book.find_element_by_css_selector('.reviews>a').get_attribute('href')
            print(link)

            content.append((book_title,book_rate,book_author,book_class,book_review))
            print(content)

        result_conent = sorted(content, key = lambda book: book[1], reverse=True)
        print(result_conent)

    def tearDown(self):
        self.dr.quit()

if __name__ == "__main__":
    unittest.main()
