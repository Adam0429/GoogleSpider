import requests
import re
import os
from tqdm import tqdm
from urllib.parse import urlencode
from requests.exceptions import ConnectionError


cookie = 'q_c1=25bc76dd511c432a83644b950d7da173|1515988249000|1515988249000; _zap=c13acc80-30d9-485d-8199-b5d7ca20d7da; aliyungf_tc=AQAAAFjMFFRg7QEAfY/PbxfHVwb82Qp/; _xsrf=896384b5-563c-4947-aec3-046e5d7789ad; d_c0="AGArvjpuDA2PTp6Ipa_pNrmXSXHhmodxuok=|1516952501"; __utmc=155987696; __utmz=155987696.1516959829.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); l_cap_id="YjFlMDY3MDYzOGU4NDJlZWI2YTQwOThkZWY5MWI5YTI=|1516962082|0b579b5d8c73c3165d5f57a602041ced94435733"; r_cap_id="ZDc0ZDg3MDQ5OWYwNDFkNmFkMmVlMGY1NDFhYzQ3NmE=|1516962082|a0c41a22f4fff204ee1acfc338c8e6cfaa4c01ca"; cap_id="NzBkOWVjYTE2YzQzNGQyNDllODRjNGYxNDk1ZmZlNTM=|1516962082|6468e04db30539e06e9c93b7cb147444738f7452"; capsion_ticket="2|1:0|10:1517069537|14:capsion_ticket|44:OWFhOWEyMDRjM2M5NDU1ZGI4MzlhNGE5NzNiZGI1M2E=|56265a049410059561f0dad12aaa36275541e5ea10c14c7ac5bdfde69c6e526b"; z_c0="2|1:0|10:1517069538|4:z_c0|92:Mi4xTFpNV0FRQUFBQUFBWUN1LU9tNE1EU1lBQUFCZ0FsVk40dkpaV3dBQnlTVWhiRzEyTzRlOVhjQUp4WFU1MVRjZ3BB|cf2ddb81d1271cbe8027dbfaf0c0fad449109c883863d096176066f57d011a62"; __utma=155987696.1069192789.1516959829.1517068365.1517071595.4'
header = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Connection':'keep-alive',
	'Cookie':cookie,
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.132 Chrome/63.0.3239.132 Safari/537.36'
}

def findquestions(word):
	questionurls = []
	index = 0
	Thread = True
	url = 'https://www.zhihu.com/api/v4/search_v3?type=general&q='+word+'&offset=1'+'&limit=20'
	r = requests.get(url,headers=header)
	if len(re.findall('questions',r.text)) == 0:
		print('no question')
		exit()
	print('正在搜索相关答案...')
	while Thread:
		url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q='+word+'&offset='+str(index)+'&limit=20'
		r = requests.get(url,headers=header)
		questions = re.findall('https:\\\/\\\/api.zhihu.com\\\/questions\\\/[0-9]+',r.text)
		if(len(questions) == 0):
			Thread = False
			break
		index = index + 20
		for q in questions:
			questionurls.append(re.findall('[0-9]+',q)[0])
		# print(questionurls)


	print('搜索到相关答案:'+str(len(questionurls)))
	return questionurls


def findanswers(question):
	index = 0
	answers = []
	Thread = True
	while Thread:
		r = requests.get('https://www.zhihu.com/api/v4/questions/'+question+'/answers?limit=20&offset='+str(index),headers=header)
		answersurl = re.findall('answers\/[0-9]+',r.text)
		if(len(answersurl) == 0):
			Thread = False
			break
		for a in answersurl:
			a = a.split('answers/')[1]
			answers.append('https://www.zhihu.com/answer/'+a)
		index = index + 20
		
	print('answers:'+str(len(answers)))
	return answers



def downloadpic(answer):

	name = answer.split('https://www.zhihu.com/answer/')[1]
	r = requests.get(answer,headers=header)
	imgs = re.findall('src=".+?"',r.text)
	imgs = set(imgs)
	n = 1
	# print((imgs))
	for img in imgs:
		img = img.split('src="')[1].split('"')[0]
		print(img)
		try:
			if len(re.findall("xs.jpg",img)) == 0 and len(re.findall("static.zhihu",img)) == 0 and len(re.findall("data:image/",img)) == 0:#throw js and user picture 
				r = requests.get(img,headers=header,stream=True,timeout=5)
				if r.status_code == 200: 
					imgtype = img[-3:]
					if not os.path.exists('/home/wangfeihong/zhihu/'+name):
						os.mkdir('/home/wangfeihong/zhihu/'+name)
					with open('/home/wangfeihong/zhihu/'+name+'/'+str(n)+'.'+imgtype,'wb') as f:
						for chunk in r.iter_content(1024): 
							f.write(chunk)
					n = n + 1
				print(str(n)+'.'+imgtype)
		except KeyboardInterrupt:
			break
		except Exception as e:
			print(e)
			pass

word = input('pls input:')
questionurls = findquestions(word)
for qs in tqdm(questionurls):
	answers = findanswers(qs)
	for a in answers:
		downloadpic(a)