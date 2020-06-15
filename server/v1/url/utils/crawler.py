from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class Crawler:
    IMAGE_404 = 'https://urlink.s3.ap-northeast-2.amazonaws.com/static/404-image.png'
    IMAGE_FAVICON = 'https://urlink.s3.ap-northeast-2.amazonaws.com/static/favicon.png'

    def get_html(self, path):
        self.path = path
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Sec-Fetch-Dest': 'document'
        }
        try:
            return requests.get(self.path, headers=headers, timeout=5).text
        except Exception as e:
            return str(e)

    def get_meta_data(self, html, keys):
        for key in keys:
            if html.find('meta', key) and html.find('meta', key).get('content'):
                return html.find('meta', key).get('content')
        return '알수없음'

    def get_favicon(self, html, keys):
        for key in keys:
            if html.find('link', key) and html.find('link', key).get('href'):
                return html.find('link', key).get('href')
        return '알수없음'

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        head = soup.head

        if not head:
            return {
                'title': '알수없음',
                'description': '알수없음',
                'image_path': self.IMAGE_404,
                'favicon_path': self.IMAGE_FAVICON
            }

        if head.title:
            title = head.title.text.strip()
        else:
            title = self.get_meta_data(head, [{'name': 'title'}, {'property': 'og:title'}])
        description = self.get_meta_data(head, [{'name': 'description'}, {'property': 'og:description'}])
        image_path = self.get_meta_data(head, [{'property': 'og:image'}, {'property': 'twitter:image'}])
        favicon_path = self.get_favicon(head, [{'rel': 'shortcut icon'}, {'rel': 'icon'}])

        if image_path == '알수없음':
            image_path = self.IMAGE_404
        if urlparse(image_path).scheme == '' and urlparse(image_path).netloc == '':
            url = urlparse(self.path)
            image_path = f"{url.scheme}://{url.netloc}{image_path}"
        elif urlparse(image_path).scheme == '' and urlparse(image_path).netloc != '':
            url = urlparse(self.path)
            image_path = f"{url.scheme}:{image_path}"

        if favicon_path == '알수없음':
            favicon_path = self.IMAGE_FAVICON
        if urlparse(favicon_path).scheme == '' and urlparse(favicon_path).netloc == '':
            url = urlparse(self.path)
            favicon_path = f"{url.scheme}://{url.netloc}{favicon_path}"
        elif urlparse(favicon_path).scheme == '' and urlparse(favicon_path).netloc != '':
            url = urlparse(self.path)
            favicon_path = f"{url.scheme}:{favicon_path}"

        return {
            'title': title,
            'description': description,
            'image_path': image_path,
            'favicon_path': favicon_path
        }


if __name__ == "__main__":
    from pprint import pprint

    c = Crawler()
    for path in ['abc', 'https://programmers.co.kr/learn/challenges?tab=all_challenges', 'https://www.acmicpc.net/',
                 'https://ssungkang.tistory.com/category/%EC%9B%B9%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D/Django',
                 'https://tech.cloud.nongshim.co.kr/techblog/', 'https://mail.google.com/mail/u/0/#inbox',
                 'https://syundev.tistory.com/29?category=868616', 'https://github.com/hotire/turnover-story',
                 'http://www.bloter.net/archives/257437',
                 'https://www.youtube.com/watch?v=r6TFnNQsQLY&feature=youtu.be',
                 'https://ofcourse.kr/css-course/cursor-%EC%86%8D%EC%84%B1']:
        html = c.get_html(path)
        pprint(c.parse_html(html))
