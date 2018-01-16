from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
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



length = 0
thread = True
b = False
done = []				#not download pictures,the pictures that have processed
i = 0
while thread:
	js = "window.scroll(0,99999999999)"
	print('page down...')
	driver.execute_script(js)
	print('page down finish')		# sleep(1)
	imgs = []

	elements = driver.find_elements(By.TAG_NAME, 'img')

	for ele in elements:
		imgs.append(ele.get_attribute('src'))

	if length == len(driver.find_elements(By.TAG_NAME, 'img')):
		button = driver.find_elements(By.ID,'smb')

		if len(button) == 0:
			print('imgs load finshed')
			thread = False	

		else:
			if b == False:			
				button[0].click()
				b = True
			else:	
				print('imgs load finshed')
				thread = False	
						
	else:
		length = len(driver.find_elements(By.TAG_NAME, 'img'))
		print('find imgs number: '+ str(length))

js = "window.scroll(0,0)"
driver.execute_script(js)
clickimg = driver.find_elements(By.TAG_NAME, 'img')
clickdone = set()	
clickdone.add(clickimg[0])
clickimg.remove(clickimg[0])
imgsdone = set()
Thread = True
n = 0
print('begin========')
while Thread:
	
	for i in tqdm(clickimg):
		try:
			# id = id + 1
			clickdone.add(i)
			i.click()
			tag_a = driver.find_elements(By.TAG_NAME, 'a')		
			for a in tag_a: 	
				if a.get_attribute('class') == 'irc_fsl i3596':
					url = a.get_attribute('href')					
					if url not in imgsdone:
						print(url)
						r = requests.get(url, stream=True,timeout=5)
						if r.status_code == 200: 
							imgtype = url[-3:]
							with open('/home/wangfeihong/pic/'+str(n)+'.'+imgtype,'wb') as f:
								for chunk in r.iter_content(1024): 
									f.write(chunk)
									# imgsdone.add(line)
								n = n + 1
								print(str(n)+'.'+imgtype)
								imgsdone.add(url)

		except KeyboardInterrupt:
			break
		except Exception as e:		
			print(e)
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
