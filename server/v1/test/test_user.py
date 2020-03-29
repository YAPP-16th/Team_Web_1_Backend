from pprint import pprint

from django.test import TestCase
from rest_framework.test import APIClient


class UserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_success_sign_up(self):
        '''
        회원가입 성공 케이스
        '''
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

    def test_fail_sign_up(self):
        '''
        회원가입 실패 케이스
        1) 이메일 형식 오류
        2) email, password, username 필드 누락
        3) password 형식 오류(6자리)
        4) email 중복
        '''
        params = {
            "email": "testnaver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

        params = {
            "email": "test@naver.com",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

        params = {
            "email": "test@naver.com",
            "password": "12312",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')

        # email 중복
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

    def test_success_sign_in(self):
        '''
        로그인 성공 케이스
        '''
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
        self.assertEqual(response.status_code, 200)

    def test_fail_sign_in(self):
        '''
        로그인 실패 케이스
        1) 필드 누락
        2) 비밀번호 오류
        3) 없는 email or password
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')

        params = {
            "email": "test@naver.com",
            # "password": "123123",
        }
        response = self.client.post('/api/v1/user/sign-in/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

        params = {
            "email": "testaver.com",
            "password": "123123",
        }
        response = self.client.post('/api/v1/user/sign-in/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

        params = {
            "email": "test@naver.com",
            "password": "1231231",
        }
        response = self.client.post('/api/v1/user/sign-in/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

        params = {
            "email": "tes2t@naver.com",
            "password": "1231231",
        }
        response = self.client.post('/api/v1/user/sign-in/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

    def test_success_sign_out(self):
        '''
        로그아웃 성공 케이스
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        token = response.json()['token']

        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 200)

    def test_fail_sign_out(self):
        '''
        로그아웃 실패 케이스
        1) 로그아웃했는데 또 로그아웃(이미 블랙리스트된 토큰인데 재 로그아웃시도)
        2) 만료된 토큰으로 로그아웃
        3) 잘못된 토큰으로 로그아웃
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        token = response.json()['token']

        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {token}'})

        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 403)

        params = {
            "email": "test2@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        token = response.json()['token']

        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {token}1'})
        pprint(response.json())
        self.assertEqual(response.status_code, 401)

        from time import sleep
        sleep(4)
        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 401)

    def test_success_get_user(self):
        '''
        get 유저 성공 케이스
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        token = response.json()['token']

        response = self.client.get('/api/v1/user/1/', **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_fail_get_user(self):
        '''
        get 유저 실패 케이스
        1) 유효하지않은 토큰으로 가져온다.
            1. 만료된 토큰
            2. 잘못된 토큰
        2) 내 토큰으로 다른 유저를 가져온다.
        3) 존재하지않는 유저를 가져온다.
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        token = response.json()['token']
        params = {
            "email": "tes1t@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')

        response = self.client.get('/api/v1/user/1/', **{'HTTP_AUTHORIZATION': f'JWT {token}1'})
        pprint(response.json())
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/api/v1/user/2/', **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/api/v1/user/3/', **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 404)

    def test_success_delete_user(self):
        '''
        delete user 성공 케이스
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        token = response.json()['token']

        response = self.client.delete('/api/v1/user/1/', **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response)
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/api/v1/user/1/', **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 401)

    def test_success_update_user(self):
        '''
        update user 성공 케이스
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        token = response.json()['token']

        params['email'] = "hi@navr.com"
        response = self.client.patch('/api/v1/user/1/', params, format='json', **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 200)

    def test_fail_update_user(self):
        '''
        update user 실패 케이스
        1) 이메일 형식
        2) 비밀번호 형식
        3) 존재하는 이메일로
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        token = response.json()['token']

        params['email'] = "hi.com"
        response = self.client.patch('/api/v1/user/1/', params, format='json', **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

        params['email'] = "test@naver.com"
        params['password'] = '12'
        response = self.client.patch('/api/v1/user/1/', params, format='json', **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

        params = {
            "email": "test1@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        params['email'] = "test1@naver.com"
        params['password'] = '1231322'
        response = self.client.patch('/api/v1/user/1/', params, format='json', **{'HTTP_AUTHORIZATION': f'JWT {token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 400)

# 구글 회원가입
# 구글 로그아웃
# 토큰
# 시리얼라이저 공부

# def test_obtain_jwt(self):
#     '''
#     회원가입할떄 얻은 유저의 jwt과 obtain_jwt이 같은 jwt을 반환하는지 test
#     :return:
#     '''
#     params = {
#         "email": "test@naver.com",
#         "password": "123123",
#         "username": "123123"
#     }
#     response = self.client.post('/api/v1/user/sign-up/', params, format='json')
#     jwt_token = response.json()['token']
#     response = self.client.post('/api/v1/user/token/', params, format='json')
#
#     self.assertEqual(jwt_token, response.json()['token'])
#     # 같다!
#
# def test_verify_jwt(self):
#     params = {
#         "email": "test@naver.com",
#         "password": "123123",
#         "username": "123123"
#     }
#     response = self.client.post('/api/v1/user/sign-up/', params, format='json')
#     jwt_token = response.json()['token']
#     token = {
#         'token': jwt_token
#     }
#     response = self.client.post('/api/v1/user/token/verify/', token, format='json')
#     print(response.json())
#     self.assertEqual(jwt_token, response.json()['token'])
# def test_refresh_jwt(self):
#        # params = {
#        #     "email": "test@naver.com",
#        #     "password": "123123",
#        #     "username": "123123"
#        # }
#        # response = self.client.post('/api/v1/user/sign-up/', params, format='json')
#        # jwt_token = response.json()['token']
#        token = {
#            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3RAbmF2ZXIuY29tIiwiZXhwIjoxNTg1Mjk1MjQzLCJlbWFpbCI6InRlc3RAbmF2ZXIuY29tIiwib3JpZ19pYXQiOjE1ODUyOTQ5NDN9.MXK8Kv0gIEO84r1dQRn4E4r_EKjhyP9GACu-e5SJyEA'
#        }
#        response = self.client.post('/api/v1/user/token/refresh/', token, format='json')
#        print(response.json())
#        # 토큰이 만료되면 새로 얻어야하나????
#        self.assertEqual(token['token'], response.json()['token'])
