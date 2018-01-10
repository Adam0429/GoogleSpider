# https://selenium-python-zh.readthedocs.io/en/latest/getting-started.html

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re

def page_down(_driver):
	length = 0
	thread = True
	while thread:
		js = "window.scroll(0,99999999999)"
		print('loading js...')
		_driver.execute_script(js)
		print('loading js finish')
		if length == len(_driver.find_elements(By.TAG_NAME, 'img')):
			print('imgs load finshed')
			thread = False
		else:
			length = len(_driver.find_elements(By.TAG_NAME, 'img'))
			print('now images number: '+ str(length))
		sleep(1)
# def download(_driver):


search_query = input('please input:')
driver = webdriver.Chrome()
driver.get('http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word='+search_query)
# driver.get('https://www.google.com.hk/search?q=search_query&source=lnms&tbm=isch')

# imgs = driver.find_elements(By.TAG_NAME, 'img')
# print(imgs[0].size)
print(driver.page_source)
# page_down(driver)

# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG, "img"))
#     )
# finally:
# 	driver.quit()

# element = wait.until(EC.element_to_be_clickable((By.ID,'someid')))
# imgs = driver.find_elements(By.TAG_NAME, 'img')
# print(len(imgs))
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
# driver.close()

