from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
import json
import requests
from time import sleep





s = requests.Session()
driver = webdriver.Chrome()

driver.get('https://mobile.qzone.qq.com')
driver.find_element_by_id('u').clear()
driver.find_element_by_id('u').send_keys('872490934')
driver.find_element_by_id('p').clear()
driver.find_element_by_id('p').send_keys('')
driver.find_element_by_id('go').click()

while True:
	print(1)
	qzonetoken = driver.execute_script("return window.shine0callback")
	if qzonetoken:
		break
	sleep(0.1)
#读取cookie后关闭浏览器
cookies = driver.get_cookies()
driver.quit()

cookies_ = {}
for cookie in cookies:
    if cookie['name'] == 'p_skey':
        skey = cookie['value']
    #s.cookies.set(cookie['name'], cookie['value'])
    cookies_[cookie['name']] = cookie['value']

#计算gtk
e = 5381
for i in range(len(skey)):
    e = e + (e<<5)+ord(skey[i])
g_tk = str(2147483647 & e)

from tqdm import tqdm
for album_uin in tqdm(range(100900,999999999)):
	try:
		album_uin = str(album_uin)
		requests.utils.add_dict_to_cookiejar(s.cookies, cookies_)
		url="https://mobile.qzone.qq.com/list?qzonetoken="+qzonetoken+"&g_tk="+g_tk+"&format=json&list_type=album&action=0&res_uin="+album_uin+"&count=50"
		r = s.get(url);
		data = json.loads(r.text)
		n = 1
	# print(data)
		for album in data['data']['vFeeds']:
			print('相册名:'+album['pic']['albumname'])
			print('相册id:'+album['pic']['albumid'])
			print('图片数量:' + str(album['pic']['albumnum']))
			print('开始下载相册图片:')
			#读取当前相册中的图片列表
			url = "https://h5.qzone.qq.com/webapp/json/mqzone_photo/getPhotoList2?qzonetoken="+qzonetoken+"&g_tk="+g_tk+"&uin="+album_uin+"&albumid="+album['pic']['albumid']+"&ps=0"
			r = s.get(url)
			photo_datas = json.loads(r.text)
			for T in photo_datas['data']['photos']:
				for pic in photo_datas['data']['photos'][T]:
					print('图片名:'+pic['picname']+'，url:'+pic['1']['url'])
					try:
						img = pic['1']['url']
						r = requests.get(img, stream=True,timeout=5)
						if r.status_code == 200: 
							imgtype = img[-3:]
							with open('/unsullied/sharefs/wangfeihong/wfh/qzone/'+album_uin+str(n)+'.'+imgtype,'wb') as f:
								for chunk in r.iter_content(1024): 
									f.write(chunk)
								n = n + 1
								print(album_uin+str(n)+'.'+imgtype)
					except Exception as e:
						print(e)
						pass
			print("="*10)
	except KeyboardInterrupt:
		break
	except:
		pass



# try:
# 	driver.find_element_by_id('QM_OwnerInfo_Icon')
# 	b = True
# except:
# 	b = False
# if b:
# 	aa = driver.find_elements(By.TAG_NAME, 'a')
# 	for a in aa:
# 		if a.get_attribute('title') == '相册':
# 			a.click()
# 			print('click')
# time.sleep(3)