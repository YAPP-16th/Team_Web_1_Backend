from django.test import TestCase
from rest_framework.test import APIClient


class UrlTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        self.access_token = response.json()['token']['access']

        params["email"] = "test2@naver.com"
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        self.access_token2 = response.json()['token']['access']

        params = {
            "name": "test"
        }

        response = self.client.post('/api/v1/category/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.category_id = response.json()['id']

        response = self.client.post('/api/v1/category/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})
        self.category_id2 = response.json()['id']

    def test_success_url_create(self):
        # 1개
        params = {
            "path": [
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004"]
        }

        response = self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 201)

        # 여러개
        params = {
            "path": [
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.phpschool.com/gnuboard4/bbs/board.php?bo_table=any&wr_id=40245",
                "https://cionman.tistory.com/44",
                "https://medium.com/@whj2013123218/%EC%9E%A5%EA%B3%A0-django-channels%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%98%EC%97%AC-%EA%B8%B0%EB%B3%B8-%EC%95%8C%EB%9E%8C-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-%EC%BD%94%EB%93%9C%ED%8E%B8-718ffc62c6c2"]
        }

        response = self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 201)

    def test_fail_url_create(self):
        '''
        URL 생성 실패 케이스
        1) 잘못된 주소(일리는없다, 왜냐하면 드래그앤드롭으로 크롬에서 이미 유효성이 검증된 url 이므로) 그럼에도 그럴 수 있으니 예외처리를 하자
        2) 없는 카테고리
        '''

        # 잘못된 주소 -> fail 에 담긴다.
        params = {
            "path": [
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.phpddddschool.com/gnuboard4/bbs/board.php?bo_table=any&wr_id=40245"
            ]
        }

        # TEST에서 request중 오류가나면 재시도하나보다.. 테스트 불가
        # response = self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
        #                             **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        #
        # self.assertEqual(response.status_code, 201)

        # 없는 카테고리
        params = {
            "path": [
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
            ]
        }
        response = self.client.post(f'/api/v1/url/?category={2}', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 500)

    def test_success_url_list(self):
        params = {
            "path": [
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.phpschool.com/gnuboard4/bbs/board.php?bo_table=any&wr_id=40245",
                "https://cionman.tistory.com/44",
                "https://medium.com/@whj2013123218/%EC%9E%A5%EA%B3%A0-django-channels%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%98%EC%97%AC-%EA%B8%B0%EB%B3%B8-%EC%95%8C%EB%9E%8C-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-%EC%BD%94%EB%93%9C%ED%8E%B8-718ffc62c6c2"]
        }

        self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
                         **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        response = self.client.get(f'/api/v1/url/?category={self.category_id}',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

    def test_success_url_filter_list(self):
        params = {
            "path": [
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.phpschool.com/gnuboard4/bbs/board.php?bo_table=any&wr_id=40245",
                "https://cionman.tistory.com/44",
                "https://medium.com/@whj2013123218/%EC%9E%A5%EA%B3%A0-django-channels%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%98%EC%97%AC-%EA%B8%B0%EB%B3%B8-%EC%95%8C%EB%9E%8C-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-%EC%BD%94%EB%93%9C%ED%8E%B8-718ffc62c6c2"]
        }

        self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
                         **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        response = self.client.get(f'/api/v1/url/?category={self.category_id}&path=php',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/api/v1/url/?category={self.category_id}&title=개',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/api/v1/url/?category={self.category_id}&란ㄹㄴㅇㄹㄴ=누울ㄴ알나란ㅇ',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

    def test_fail_url_list(self):
        '''
        URL 리스트 조회 실패 케이스
        1) 없는 카테고리
        '''

        params = {
            "path": [
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.phpschool.com/gnuboard4/bbs/board.php?bo_table=any&wr_id=40245",
                "https://cionman.tistory.com/44",
                "https://medium.com/@whj2013123218/%EC%9E%A5%EA%B3%A0-django-channels%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%98%EC%97%AC-%EA%B8%B0%EB%B3%B8-%EC%95%8C%EB%9E%8C-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-%EC%BD%94%EB%93%9C%ED%8E%B8-718ffc62c6c2"]
        }

        self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
                         **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        # 잘못된 카테고리 번호 입력해도 에러는 아닌것으로
        response = self.client.get(f'/api/v1/url/?category=999',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

    def test_success_url_delete(self):
        params = {
            "path": [
                "https://medium.com/@whj2013123218/%EC%9E%A5%EA%B3%A0-django-channels%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%98%EC%97%AC-%EA%B8%B0%EB%B3%B8-%EC%95%8C%EB%9E%8C-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-%EC%BD%94%EB%93%9C%ED%8E%B8-718ffc62c6c2"]
        }

        self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
                         **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        response = self.client.delete(f'/api/v1/url/1/',
                                      **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 204)

    def test_fail_url_delete(self):
        '''
        URl 삭제 실패 케이스
        1) 없는 pk로 삭제
        2) 권한이 없는 URL 삭제
        '''

        params = {
            "path": [
                "https://medium.com/@whj2013123218/%EC%9E%A5%EA%B3%A0-django-channels%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%98%EC%97%AC-%EA%B8%B0%EB%B3%B8-%EC%95%8C%EB%9E%8C-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-%EC%BD%94%EB%93%9C%ED%8E%B8-718ffc62c6c2"]
        }

        self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
                         **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        # 1) 없는 pk로 삭제
        response = self.client.delete(f'/api/v1/url/2/',
                                      **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 404)
        # 2) 권한이 없는 URL 삭제
        response = self.client.delete(f'/api/v1/url/1/',
                                      **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})

        self.assertEqual(response.status_code, 403)

    def test_success_url_update(self):
        params = {
            "path": [
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004"]
        }

        response = self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 201)

        params = {
            'is_favorited': 'true',
            'description': '호옹이'

        }
        response = self.client.patch(f'/api/v1/url/1/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/api/v1/url/?category={self.category_id}',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.json()[0]['id'], 1)
        self.assertEqual(response.json()[0]['description'], '호옹이')

    def test_fail_url_update(self):
        '''
        URl 업데이트 실패 케이스
        1. path 수정
        2) 권한이 없는 URL 업데이트
        3) Put method 요청
        '''
        params = {
            "path": [
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004",
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004"]
        }

        response = self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        response = self.client.post(f'/api/v1/url/?category={self.category_id2}', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})
        self.assertEqual(response.status_code, 201)

        # 1. path 수정
        params = {
            'path': 'https://naver.com',
            'is_favorited': 'true',
            'description': '호옹이'

        }
        response = self.client.patch(f'/api/v1/url/1/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 500)

        # 2. 권한이 없는 URL 업데이트
        params = {
            'path': 'https://naver.com',
            'is_favorited': 'true',
            'description': '호옹이'
        }
        response = self.client.patch(f'/api/v1/url/7/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 403)

        # 3. Put method 요청
        params = {
            'path': 'https://naver.com',
            'is_favorited': 'true',
            'description': '호옹이'
        }
        response = self.client.put(f'/api/v1/url/1/', params, format='json',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 500)
