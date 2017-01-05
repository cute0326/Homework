from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

class QQDailyHot():
    def __init__(self):
        self.dr = webdriver.Firefox()
        self.title,self.content = self.DailyHot_content_and_title()

    def QQHotLink(self):
        self.dr.get('http://qq.com')
        return(self.dr.find_element_by_css_selector('#todaytop>a').get_attribute('href'))

    def DailyHot_content_and_title(self):
        self.dr.get(self.QQHotLink())
        title = self.dr.find_element_by_id('sharetitle').text
        content = self.dr.find_element_by_id('articleContent').get_attribute('innerHTML')
        return(title,content)

    def login_as_admin(self):
        user = 'admin'
        password = '211282'
        self.login(user,password)

    def login(self,username,password):
        self.dr.get('http://localhost/wordpress/wp-login.php')
        self.find_id('user_login').clear()
        self.find_id('user_login').send_keys(username)
        self.find_id('user_pass').clear()
        self.find_id('user_pass').send_keys(password)
        self.find_id('wp-submit').click()
        sleep(3)   #登录怎么也登录不进去，找元素也找不到了，弄了半天，原来是firefox反应慢，需要加一个sleep才行。

    def post_in(self):
        self.login_as_admin()
        self.dr.get('http://localhost/wordpress/wp-admin/post-new.php')
        self.find_id('title').send_keys(self.title)
        content = self.content.strip()
        js = "document.getElementById('content_ifr').contentWindow.document.body.innerHTML = '%s' " %(content)
        print(js)
        self.dr.execute_script(js)
        self.find_id('publish').click()

    def find_id(self,id):
        return self.dr.find_element_by_id(id)

    def find_css(self,id):
        return self.dr.find_element_by_css_selector(id)

    def quit(self):
        return self.dr.quit()

if __name__ == '__main__':
    QQ = QQDailyHot()
    QQ.post_in()
    QQ.quit()