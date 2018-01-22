import requests
import re
from tqdm import tqdm
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

# <img src="https://pics.onsizzle.com/diogenes-5h-the-whole-i-boned-your-mom-schtick-really-stings-30227419.png" class="mainImage" title="查看源图" alt="mom 的图像结果">
# 
# word = input('pls input:')

# r = requests.get('https://cn.bing.com/images/search?view=detailV2&q=mom&first=1&selectedindex=956&id=08EEFEC0117F51887763888C49432E0486DB02DE&ccid=dqIvHmUt&simid=608022179798188449&thid=OIP.dqIvHmUt7w894eEsHf-GkwHaF1')
contents = ['哥哥弟弟','爸爸儿子','妈妈女儿','表哥表弟','表姐表妹','兄弟姐妹','家庭合照','全家福','三胞胎','四胞胎','三弟兄']
for word in contents:
	driver = webdriver.Chrome()
	driver.get('https://pic.sogou.com/d?query='+word+'&mode=1&did=1#did1')
	from time import sleep 
	kw = driver.find_element_by_id("btnPgRgt")
	n = 0
	Thread = True
	while Thread:
		sleep(0.2)
		try:	
			kw.click()	# To check if it is the last one
		except:
			print('the last one')
			Thread = False
			# driver.close()
			pass
		imgs = driver.find_elements(By.TAG_NAME, 'img')
		print(len(imgs))
		last = None
		for img in imgs:
			try:	
				if img.get_attribute('title') == '点击查看源网页': 
					print(img.get_attribute('src'))
					r = requests.get(img.get_attribute('src'), stream=True,timeout=5)
					if r.status_code == 200: 
						imgtype = img.get_attribute('src')[-3:]
						with open('/home/wangfeihong/sogou/'+word+str(n)+'.'+imgtype,'wb') as f:
							for chunk in r.iter_content(1024): 
								f.write(chunk)
							n = n + 1
							print(word+str(n)+'.'+imgtype)
			except StaleElementReferenceException:
				pass	
			except Exception as e:
				print(e)
				pass
# # print(r.text)
# imgs = re.findall('Json',r.text)
# print(len(imgs))

