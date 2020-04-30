import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, url):
        self.url = url

    def get_html(self):
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Sec-Fetch-Dest': 'document',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        response = requests.get(self.url, headers=headers)
        assert response.ok, response.reason

        return response.text

    def parse_html(self, html):
        dom = BeautifulSoup(html, 'html.parser')

        title = dom.head.find('meta', {'name': ['title']}).get('content')

        description = dom.head.find('meta', {'name': ['description']}).get('content')

        image = dom.head.find('meta', {'property': ['og:image']}).get('content')

        url_item = {'url': self.url, 'title': title, 'description': description, 'image': image}

        return url_item

if __name__ == "__main__":
    c = Crawler('https://dooa159.tistory.com/entry/ORA29275-%EB%B6%80%EB%B6%84-%EB%8B%A4%EC%A4%91-%EB%B0%94%EC%9D%B4%ED%8A%B8-%EB%AC%B8%EC%9E%90-error-%ED%95%B4%EA%B2%B0%EB%B2%95')
    html = c.get_html()
    print(c.parse_html(html))
