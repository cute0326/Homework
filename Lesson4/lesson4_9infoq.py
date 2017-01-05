#coding:utf-8
from selenium import webdriver
import time,sys

class infoq():
	"""docstring for infoq"""
	def __init__(self):
		self.dr=webdriver.Firefox()
		self.dr.implicitly_wait(8)

	def get_artices(self):
		self.dr.get("http://www.infoq.com/cn/testing/")
		root_element=self.by_css_selector(".news")
		artice_elements=root_element.find_elements_by_css_selector(".art_title")
		artices=[]
		for i in xrange(len(artice_elements)):
			self.dr.get("http://www.infoq.com/cn/testing/")
			root_element=self.by_css_selector(".news")
			artice_elements=root_element.find_elements_by_css_selector(".art_title")
			title=artice_elements[i].get_attribute("title")
			href=artice_elements[i].get_attribute("href")
			self.dr.get(href)
			artice_html=self.by_css_selector(".text_info").get_attribute("innerHTML")
			artices.append((title,artice_html))
		return artices

	def login_wordpress(self):
		self.dr.get('http://localhost/wordpress/wp-login.php')
		username='admin'
		password='19860721'
		self.by_name('log').send_keys(username)
		self.by_name('pwd').send_keys(password)
		self.by_name('wp-submit').click()

	def wordpress_publish(self,artices):
		self.login_wordpress()

		for i in xrange(len(artices)):
			self.dr.get('http://localhost/wordpress/wp-admin/post-new.php')
			self.by_name('post_title').send_keys(artices[i][0])
			self.set_content(artices[i][1])
			self.by_name('publish').click()


	def set_content(self,content):
		#strip()非常重要，去掉代码中空白符（包括'\n', '\r',  '\t',  ' ')
		content = content.strip()
		js = 'document.getElementById("content_ifr").contentWindow.document.body.innerHTML=\'%s\'' %(content)
		self.dr.execute_script(js)

	def by_id(self,this_id):
		return self.dr.find_elements_by_id(this_id)

	def by_name(self,name):
		return self.dr.find_element_by_name(name)

	def by_elements_css(self,css_selector):
		return self.dr.find_elements_by_css_selector(css_selector)

	def by_css_selector(self,css_selector):
		return self.dr.find_element_by_css_selector(css_selector)

	def by_link_text(self,link_text):
		return self.dr.find_element_by_link_text(link_text)

	def tearDown(self):
		self.dr.quit()

if __name__ == '__main__':
	infoq=infoq()
	artices=infoq.get_artices()
	infoq.wordpress_publish(artices)
	infoq.tearDown()
