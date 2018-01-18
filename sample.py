from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm
from PIL import Image
from io import BytesIO
from time import sleep
from tqdm import tqdm
import re
import requests
import base64

contents = ['爸爸儿子','妈妈女儿','表哥表弟','表姐表妹','兄弟姐妹','家庭合照','全家福','三胞胎','四胞胎','三弟兄']

# search_query = input('please input:')
for search_query in  tqdm(contents):
	driver = webdriver.Chrome()
	driver.get('https://www.google.com/search?q='+search_query+'&newwindow=1&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi9mdCtmdnYAhXLv7wKHfaGBWEQ_AUIDygA&biw=1300&bih=951')


	clickimg = driver.find_elements(By.TAG_NAME, 'img')
	clickdone = set()	
	clickdone.add(clickimg[0])
	clickimg.remove(clickimg[0])
	imgsdone = set()
	Thread = True
	n = 0
	cur = 1
	length = len(clickimg)
	print('begin========')
	while Thread:

		try:
			cur = cur + 1
			clickimg[cur].click()
			sleep(0.5)
			clickimg[cur].click()
			clickdone.add(clickimg[cur])
			print('len: '+str(len(clickimg)))
			print('cur: '+str(cur))
			tag_a = driver.find_elements(By.TAG_NAME, 'a')		
			for a in tag_a: 	
				if a.get_attribute('class') == 'irc_fsl i3596':
					url = a.get_attribute('href')					
					if url not in imgsdone:
						print(url)
						r = requests.get(url, stream=True,timeout=5)
						if r.status_code == 200: 
							imgtype = url[-3:]
							with open('/home/wangfeihong/pic/'+search_query+str(n)+'.'+imgtype,'wb') as f:
								for chunk in r.iter_content(1024): 
									f.write(chunk)
									# imgsdone.add(line)
								n = n + 1
								print(search_query+str(n)+'.'+imgtype)
								imgsdone.add(url)
		except KeyboardInterrupt:
			break
		except Exception as e:
			print('len: '+str(len(clickimg)))
			print('cur: '+str(cur))
			print(e)
			clickimg = driver.find_elements(By.TAG_NAME, 'img')
			if len(clickimg) < cur:
				Thread = False 
			pass



# ii = []

# n = 0
# for line in tqdm(file.readlines()):
# 	try:
# 		# if line not in imgsdone: 
# 		r = requests.get(line, stream=True,timeout=15)
# 		if r.status_code == 200: 
# 			imgtype = line[-3:]
# 			with open('/home/wangfeihong/pic/'+str(n)+'.'+imgtype,'wb') as f:
# 				for chunk in r.iter_content(1024): 
# 					f.write(chunk)
# 				# imgsdone.add(line)
# 				n = n + 1
# 				print(str(n)+'.'+imgtype)
# 	except KeyboardInterrupt:
# 		break
# 	except Exception as e:
# 		print(e)
# 		pass

# # clickdone = set()
# # clickdone.add(clickimg[0])
# # clickimg.remove(clickimg[0])
# # imgs = set()
# # imgsdone = set()
# # n = 0
# # while True:
# # 	try:
# # 		for i in tqdm(clickimg):
# # 			clickdone.add(i)
# # 			i.click()
# # 			tag_a = driver.find_elements(By.TAG_NAME, 'a')		
# # 			for a in tag_a: 	
# # 				if a.get_attribute('class') == 'irc_fsl i3596':
# # 					url = a.get_attribute('href')
# # 					imgs.add(url)
# # 			if url not in imgsdone: 
# # 				r = requests.get(url, stream=True,timeout=15)
# # 				if r.status_code == 200: 
# # 					n = n + 1
# # 					imgtype = url[-3:]
# # 					with open('/home/wangfeihong/pic/'+str(n)+'.'+imgtype,'wb') as f:
# # 						for chunk in r.iter_content(1024): 
# # 							f.write(chunk)
# # 						imgsdone.add(url)
# # 						print(str(n)+'.'+imgtype)
# # 			# sleep(0.5)
# # 	except Exception as e:
# # 		print(e)
# # 		clickimg = driver.find_elements(By.TAG_NAME, 'img')
# # 		for d in clickdone:
# # 			if d in clickimg:
# # 				clickimg.remove(d)
# # 		pass
