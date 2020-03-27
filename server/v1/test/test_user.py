from pprint import pprint

from django.test import TestCase
from rest_framework.test import APIClient


class UserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_sign_up(self):
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 201)

        params['email'] = 'abc@aaa.com'
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 201)

    def test_obtain_jwt(self):
        '''
        회원가입할떄 얻은 유저의 jwt과 obtain_jwt이 같은 jwt을 반환하는지 test
        :return:
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        jwt_token = response.json()['token']
        response = self.client.post('/api/v1/user/token/', params, format='json')

        self.assertEqual(jwt_token, response.json()['token'])
        # 같다!

    def test_verify_jwt(self):
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        jwt_token = response.json()['token']
        token = {
            'token': jwt_token
        }
        response = self.client.post('/api/v1/user/token/verify/', token, format='json')
        print(response.json())
        self.assertEqual(jwt_token, response.json()['token'])

    def test_refresh_jwt(self):
        # params = {
        #     "email": "test@naver.com",
        #     "password": "123123",
        #     "username": "123123"
        # }
        # response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        # jwt_token = response.json()['token']
        token = {
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3RAbmF2ZXIuY29tIiwiZXhwIjoxNTg1Mjk1MjQzLCJlbWFpbCI6InRlc3RAbmF2ZXIuY29tIiwib3JpZ19pYXQiOjE1ODUyOTQ5NDN9.MXK8Kv0gIEO84r1dQRn4E4r_EKjhyP9GACu-e5SJyEA'
        }
        response = self.client.post('/api/v1/user/token/refresh/', token, format='json')
        print(response.json())
        # 토큰이 만료되면 새로 얻어야하나????
        self.assertEqual(token['token'], response.json()['token'])

    def test_sign_in(self):
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        params = {
            "email": "test@naver.com",
            "password": "123123",
        }
        response = self.client.post('/api/v1/user/sign-in/', params, format='json')
        pprint(response.json())

    def test_sign_out(self):
        '''
        보류
        :return:
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        params = {
            "token": response.json()['token']
        }
        print({'Authorization': f'JWT {response.json()["token"]}'})
        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'Authorization': f'JWT {response.json()["token"]}'})
        pprint(response.json())

    def test_list_parking_known_query_praams2(self):
        params = {
            'addr': '율현동'
        }
        self.parking1.save()
        self.parking2.save()
        response = self.client.get('/server/parking/', data=params, content_type='application/json')
        pprint(response.json())

# 로그아웃
# 구글 회원가입
# 구글 로그아웃
# 객체생성
# 권한확인
# 객체가져오기
# 에러객체 통

# 시리얼라이저 공부
