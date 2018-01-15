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



search_query = input('please input:')

driver = webdriver.Chrome()
driver.get('https://www.google.com/search?q='+search_query+'&newwindow=1&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi9mdCtmdnYAhXLv7wKHfaGBWEQ_AUIDygA&biw=1300&bih=951')
# print('imglist:'+str(len(imglist)))
img = driver.find_elements(By.TAG_NAME, 'img')

imgs = set()
done = set()
n = 0
for i in tqdm(img[2:100]):
	try:
		i.click()
		sleep(0.5)
		tag_a = driver.find_elements(By.TAG_NAME, 'a')
		for a in tag_a: 
			if a.get_attribute('class') == 'irc_fsl i3596':
				url = a.get_attribute('href')	
				print(url)
				imgs.add(url)
				# sleep(0.5)
				if url not in done: 
					r = requests.get(url, stream=True,timeout=15)
					if r.status_code == 200: 
						n = n + 1
						imgtype = url[-3:]
						with open('/home/wangfeihong/pic/'+str(n)+'.'+imgtype,'wb') as f:
							for chunk in r.iter_content(1024): 
								f.write(chunk)
							done.add(url)
							print(str(n)+'.'+imgtype)
		i.click()			
	except Exception as e:
		print(e)
		sleep(0.5)
		pass	
