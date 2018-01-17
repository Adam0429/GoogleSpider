import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
# 获得索引页的信息
#而这个链接中的的  rn 参数指的是一页包含的图片数量，最多60。 pn 指得是第多少张  word 指的是搜索的关键字，其它的一些参数是无关紧要的， 当然你需要把其转码
word = input('pls input:')
base_url = 'http://image.baidu.com/search/acjson?'
header1={
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
     "referer":"https://image.baidu.com"
}
params1={
    'queryWord':word,
    'rn':'60',
    'pn':'1'
}
r = requests.get(base_url,headers=header1,params=params1)
result = r.json()
print(type(result), result, sep='\n')
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