import requests
import re
from tqdm import tqdm
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
# 获得索引页的信息
#而这个链接中的的  rn 参数指的是一页包含的图片数量，最多60。 pn 指得是第多少张  word 指的是搜索的关键字，其它的一些参数是无关紧要的， 当然你需要把其转码

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
    toLang = ['en','jp','kor','fra','spa','th','ru','pt','de']
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
# word = input('pls input:')
contents = ['爸爸儿子','妈妈女儿','表哥表弟','表姐表妹','兄弟姐妹','家庭合照','全家福','三胞胎','四胞胎','三弟兄']
for w in contents:
    words = translate(w)
    for word in words:
        n = 1
        pn = 1
        Thread = True
        images = set()
        length = 0
        while Thread:
            base_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord='+word+'&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word='+word+'&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=girl&pn='+str(pn)+'&rn=60&gsm=1e00000000001e&1490169411926='
            r = requests.get(base_url)
            imgs = re.findall('thumbURL\":\".+?\"',r.text)
            for img in tqdm(imgs):
                images.add(img)
                img = img.split('thumbURL\":\"')[1].split('\"')[0]
                # print(img)
                try:
                    r = requests.get(img, stream=True,timeout=5)
                    if r.status_code == 200: 
                        imgtype = img[-3:]
                        with open('/home/wangfeihong/baidu/'+word+str(n)+'.'+imgtype,'wb') as f:
                            for chunk in r.iter_content(1024): 
                                f.write(chunk)
                            n = n + 1
                        print(word+str(n)+'.'+imgtype)
                except Exception as e:
                    print(e)
                    pass
            if len(images) < pn:
                Thread = False 
            pn = pn + 60    
            # print(img)
        
# print(len(imgs))
# print(type(result), result, sep='\n')
# params = urlencode(data)
# url = base_url + params
# try:
#     resp = requests.get(url)
#     if resp.status_code == 200:
#        return resp.text
#     return None
# except ConnectionError:
#     print('Error.')
#     return None