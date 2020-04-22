import requests
from bs4 import BeautifulSoup
header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}


def getDownload(url, param=None, retries=3):
    resp = None
    try:
        resp = requests.get(url, params=param, headers=header)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if 500 <= resp.status_code < 600 and retries > 0:
            print('Retries : {0}'.format(retries))
            return getDownload(url, param, retries - 1)
        else:
            print(resp.status_code)
            print(resp.reason)
            print(resp.request.headers)

    return resp

url = 'https://dooa159.tistory.com/entry/ORA29275-%EB%B6%80%EB%B6%84-%EB%8B%A4%EC%A4%91-%EB%B0%94%EC%9D%B4%ED%8A%B8-%EB%AC%B8%EC%9E%90-error-%ED%95%B4%EA%B2%B0%EB%B2%95'

html = getDownload(url)
dom = BeautifulSoup(html.text,'html.parser')
print("---------------------------------title--------------------------------------------")
print(dom.head.find('meta',{'name':['title']}).get('content'))
#for meta in dom.head.find_all('meta',{'name':['title']}):
#    print(meta.get('content'))
print("---------------------------------description--------------------------------------------")
print(dom.head.find('meta',{'name':['description']}).get('content'))
#for meta in dom.head.find('meta',{'name':['description']}):
#    print(meta.get('content'))
print("---------------------------------og:image--------------------------------------------")
print(dom.head.find('meta',{'property':['og:image']}).get('content'))
#for meta in dom.head.find('meta',{'property':['og:image']}):
#    print(meta.get('content'))