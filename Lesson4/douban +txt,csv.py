from selenium import webdriver
import unittest
from time import sleep
import csv

class DOUBAN(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.Firefox()

    def goto_web(self):
        self.dr.get('https://movie.douban.com/nowplaying/shenzhen/')
        # print(self.dr.current_url)

    def test_movie_list(self):
        self.goto_web()
        on_playing = self.dr.find_element_by_css_selector('.lists')
        movies = on_playing.find_elements_by_css_selector('.list-item')

        self.write_num_to_txt(movies,15)
        self.write_num_to_csv(movies,15)

    def write_num_to_txt(self, movies,number):
        f = open('..\\result.txt','w+')
        count = 0
        for movie in movies:
            content = ''
            title = movie.get_attribute('data-title')
            print((title))
            score = movie.get_attribute('data-score')
            print(score)

            content = title + ':' + score + ';'
            f.write(content)
            f.write('\n')
            count = count + 1

            if count>=number:
                break
        f.close()

    def write_num_to_csv(self, movies,number):
            f = open('..\\result.csv','w+')
            count = 0
            for movie in movies:
                content = ''
                title = movie.get_attribute('data-title')
                print((title))
                score = movie.get_attribute('data-score')
                print(score)

                content = title + ',' + score
                f.write(content)
                f.write('\n')
                count = count + 1

                if count>=number:
                    break
            f.close()

    def tearDown(self):
        self.dr.quit()

if __name__ == "__main__":
    unittest.main()
