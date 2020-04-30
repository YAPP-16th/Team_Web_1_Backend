import requests
from bs4 import BeautifulSoup

from server.exceptions import ServerException


class Crawler:
    def __init__(self, path):
        self.path = path

    def get_html(self):
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Sec-Fetch-Dest': 'document'
        }

        response = requests.get(self.path, headers=headers)
        if not response.ok:
            raise ServerException(response.reason)

        return response.text

    def get_meta_data(self, html, keys):
        for key in keys:
            if html.find('meta', key) and html.find('meta', key).get('content'):
                return html.find('meta', key).get('content')
        return '알수없음'

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        head = soup.head

        title = head.title.text.strip() if head.title else self.get_meta_data(head,
                                                                              [{'name': 'title'},
                                                                               {'property': 'og:title'}])
        description = self.get_meta_data(head, [{'name': 'description'}, {'property': 'og:description'}]).strip()
        image_path = self.get_meta_data(head, [{'property': 'og:image'}, {'property': 'twitter:image'}])

        if image_path == '알수없음':
            image_path = 'https://www.boostability.com/wp-content/uploads/2012/10/BOOST_BLOG_IMAGE_RB_SET_10_404_PAGE_1200x628px_v1_3.jpg'

        return {
            'path': self.path,
            'title': title,
            'description': description,
            'image_path': image_path
        }


if __name__ == "__main__":
    from pprint import pprint

    for url in ['https://programmers.co.kr/learn/challenges?tab=all_challenges', 'https://www.acmicpc.net/',
                'https://ssungkang.tistory.com/category/%EC%9B%B9%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D/Django',
                'https://tech.cloud.nongshim.co.kr/techblog/', 'https://mail.google.com/mail/u/0/#inbox',
                'https://syundev.tistory.com/29?category=868616', 'https://github.com/hotire/turnover-story',
                'http://www.bloter.net/archives/257437',
                'https://www.youtube.com/watch?v=r6TFnNQsQLY&feature=youtu.be']:
        c = Crawler(url)
        html = c.get_html()
        pprint(c.parse_html(html))
