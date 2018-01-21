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


# <img src="https://pics.onsizzle.com/diogenes-5h-the-whole-i-boned-your-mom-schtick-really-stings-30227419.png" class="mainImage" title="查看源图" alt="mom 的图像结果">
# 
word = input('pls input:')

# r = requests.get('https://cn.bing.com/images/search?view=detailV2&q=mom&first=1&selectedindex=956&id=08EEFEC0117F51887763888C49432E0486DB02DE&ccid=dqIvHmUt&simid=608022179798188449&thid=OIP.dqIvHmUt7w894eEsHf-GkwHaF1')
driver = webdriver.Chrome()
driver.get('https://cn.bing.com/images/search?view=detailV2&q='+word+'&first=1&selectedindex=1')
from time import sleep 
kw = driver.find_element_by_id("iol_navr")
n = 1
while True:
	sleep(0.5)
	kw.send_keys(Keys.RIGHT)
	imgs = driver.find_elements(By.TAG_NAME, 'img')
	# print(len(imgs))
	for img in imgs:
		try:
			# need to check if it is the last one
			if img.get_attribute('class') == 'mainImage accessible nofocus':
				print(img.get_attribute('src'))
			
				r = requests.get(img.get_attribute('src'), stream=True,timeout=5)
				if r.status_code == 200: 
					imgtype = img.get_attribute('src')[-3:]
					with open('/home/wangfeihong/bing/'+word+str(n)+'.'+imgtype,'wb') as f:
						for chunk in r.iter_content(1024): 
							f.write(chunk)
							n = n + 1
						print(word+str(n)+'.'+imgtype)
		except Exception as e:
			print(e)
			pass
# # print(r.text)
# imgs = re.findall('Json',r.text)
# print(len(imgs))

