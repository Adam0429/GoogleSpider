# https://selenium-python-zh.readthedocs.io/en/latest/getting-started.html

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from PIL import Image
from io import BytesIO
from time import sleep
import re
import requests
import base64

def download(_driver,name,translate=False):
	length = 0
	thread = True
	done = []
	i = 0
	while thread:
		js = "window.scroll(0,99999999999)"
		print('page down...')
		_driver.execute_script(js)
		print('page down finish')

		imgs = []

		elements = driver.find_elements(By.TAG_NAME, 'img')


		for ele in elements:
			imgs.append(ele.get_attribute('src'))

		for img in tqdm(imgs[len(done):len(imgs)]): 
			
			try:
				done.append(img)
				if img is None:
					pass
				if len(img) < 300:
					r = requests.get(img, stream=True,timeout=5) 
				
					if r.status_code == 200: 
						i = i + 1
						# imgtype = img[-3:]
						with open('/home/wangfeihong/pic/'+name+str(i)+'.'+'jpeg','wb') as f:
							for chunk in r.iter_content(1024): 
								f.write(chunk)
							print(name+str(i)+'.'+'jpeg')
				
				else:
					i = i + 1
					imgtype = img.split('data:image//')[0].split(';base64')[0].split('/')[1]
					# print(imgtype)
					img = img.split(';base64,')[1]
					img = base64.b64decode(img) 
					with open('/home/wangfeihong/pic/'+name+str(i)+'.'+imgtype,'wb') as f: 
						f.write(img)
						print(name+str(i)+'.'+imgtype)
				
			except KeyboardInterrupt:
				break			
			except Exception as e:
				pass
		

		if length == len(_driver.find_elements(By.TAG_NAME, 'img')):
			button = _driver.find_elements(By.ID,'smb')
			if len(button) == 0:
				print('imgs load finshed')
				thread = False
				_driver.quit()
			else:
				button[0].click()
		else:
			length = len(_driver.find_elements(By.TAG_NAME, 'img'))
			print('find imgs number: '+ str(length))

def translate(word):
	import urllib2, json, urllib 

	data = {}
	data["appkey"] = "your_appkey_here"
	data["type"] = "google"
	data["from"] = "zh-CN"
	data["to"] = "en"
	data["text"] = "书"
 
	url_values = urllib.urlencode(data)
	url = "http://api.jisuapi.com/translate/translate" + "?" + url_values
	request = urllib2.Request(url)
	result = urllib2.urlopen(request)
	jsonarr = json.loads(result.read())
 
	# if jsonarr["status"] != u"0":
	#     print jsonarr["msg"]
	#     exit()
	# result = jsonarr["result"]
	# print result["result"]



search_query = input('please input:')
driver = webdriver.Chrome()
# driver.get('http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word='+search_query)
driver.get('https://www.google.com.hk/search?q='+search_query+'&source=lnms&tbm=isch')

print(translate(search_query))

# print(driver.page_source)


# try:	
# 	download(driver,search_query)
# except:
# 	print('download finish')

assert "No results found." not in driver.page_source