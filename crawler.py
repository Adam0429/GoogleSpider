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
from tqdm import tqdm
import re
import requests
import base64

def download(_driver,name):
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
			_driver.quit()

def translate(word):
	import http.client
	import hashlib
	from urllib import parse
	import random

	words = []
	appid = '20180113000114961'
	secretKey = 'i44gpYaLOWY7YhRdr7jj'
	httpClient = None

	q = word
	fromLang = 'auto'
	toLang = ['zh','en','jp','kor','fra','spa','th','ru','pt','de']
	salt = str(random.randint(32768, 65536))
	sign = appid+q+salt+secretKey
	m1 = hashlib.md5()
	m1.update(sign.encode(encoding='utf-8'))
	sign = m1.hexdigest()

	try:
		for tl in toLang:	
			httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
			myurl = '/api/trans/vip/translate'
			myurl = myurl+'?appid='+appid+'&q='+parse.quote(q)+'&from='+fromLang+'&to='+tl+'&salt='+str(salt)+'&sign='+sign 		
			httpClient.request('GET', myurl)
			response = httpClient.getresponse()
			string = response.read().decode('utf-8')
			string = eval(string) #str to dict
			words.append(string['trans_result'][0]['dst'])

	except Exception as e:
	    print(e)
	    pass
	finally:
	    if httpClient:
	        httpClient.close()
	        print(words)
	return words



search_query = input('please input:')


words = translate(search_query)

for word in words:
	driver = webdriver.Chrome()
	driver.get('https://www.google.com.hk/search?q='+word+'&source=lnms&tbm=isch')
	print('begin download ' + word + ':')
	download(driver,word)
	
assert "No results found." not in driver.page_source