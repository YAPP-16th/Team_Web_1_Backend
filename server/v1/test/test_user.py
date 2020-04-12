from pprint import pprint
from time import sleep

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

        access_token = response.json()['token']['access']
        refresh_token = response.json()['token']['refresh']

        params = {
            "refresh": refresh_token
        }
        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {access_token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 200)

    def test_fail_sign_out(self):
        '''
        로그아웃 실패 케이스
        1) 로그아웃했는데 또 로그아웃(이미 블랙리스트된 리프레시 토큰인데 재 로그아웃시도)
        2) 만료된 토큰으로 로그아웃 (로그아웃 실패, 클라이언트가 토큰을 리프레시하고 재 요청하는것으로)
        3) 잘못된 토큰으로 로그아웃
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')

        access_token = response.json()['token']['access']
        refresh_token = response.json()['token']['refresh']

        params = {
            "refresh": refresh_token
        }

        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {access_token}'})

        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {access_token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 500)
        # --------------------------------------------------------------------------------------------------------
        params = {
            "email": "test2@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')

        access_token = response.json()['token']['access']
        refresh_token = response.json()['token']['refresh']

        params = {
            "refresh": refresh_token
        }

        sleep(4)
        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {access_token}'})
        pprint(response.json())
        self.assertEqual(response.status_code, 401)
        # --------------------------------------------------------------------------------------------------------
        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {access_token}1'})
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
        token = response.json()['token']['access']

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
        token = response.json()['token']['access']
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
        token = response.json()['token']['access']

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
        token = response.json()['token']['access']

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

    def test_success_google_sign_up(self):
        '''
        google 회원가입 성공 케이스
        '''
        token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1N2Y2YTU4MjhkMWU0YTNhNmEwM2ZjZDFhMjQ2MWRiOTU5M2U2MjQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDAyMDg4ODQ3NDMxLWo1azRsNXRhbGpoZjhycGVuYWpybHFnMWgxMTg3ZHI1LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTAwMjA4ODg0NzQzMS0zZWo5M3F1Mm9sYms1bWJoaG1pamwyYjlpNWY5Nmw4ay5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExMzEyNTAzMTY1OTQ4OTI5Mjg4NSIsImVtYWlsIjoiamp1bjk0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoianVueWVvbmcgY2hvaSIsInBpY3R1cmUiOiJodHRwczovL2xoNi5nb29nbGV1c2VyY29udGVudC5jb20vLUtucTRFVVNuWTVVL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FBS1dKSk9INzV1TEFVWVhnMkRGWWFoT2thZFBKVGpVUGcvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6Imp1bnllb25nIiwiZmFtaWx5X25hbWUiOiJjaG9pIiwibG9jYWxlIjoia28iLCJpYXQiOjE1ODU4MTM1NTksImV4cCI6MTU4NTgxNzE1OX0.f4OnZu0EoUrX24qG4PuahP2Eyaz3H957tA586BLv_gD5xXlERdqQLLbJyD3-gH0Dd24r-RErsU9zxKOa86YXHsAHLdtmlLZ4LJrOyp1EiEQFTdUqvYdFEbtxCFWRz0F2Grcntun2Pj9md_odddemTgzEaE1OWKxnJRqe_3eD9P6EjY380wvwveP8wZZqLW6LKg9fR8sPVwqZ_sYhlGvVWpqworLLibTrG55D_-KsN_DfLzSuPLXAQuWAjCBfvzTc9p-EICiroMgAvBVDeRsH98uM0c9iT42gqXGNBM2bhcfUMAuWOKDwRFU3k0GYYlKiYwJnofdY2nyKMFAunwe6XQ'

        params = {
            "token": token,
        }
        response = self.client.post('/api/v1/user/google/sign-up/', params, format='json')
        pprint(response.json())

    def test_fail_google_sign_up(self):
        '''
        google 회원가입 실패 케이스
        1) 토큰이 유효하지 않음.
        2) 이미 가입된 유저
        '''
        token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1N2Y2YTU4MjhkMWU0YTNhNmEwM2ZjZDFhMjQ2MWRiOTU5M2U2MjQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDAyMDg4ODQ3NDMxLWo1azRsNXRhbGpoZjhycGVuYWpybHFnMWgxMTg3ZHI1LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTAwMjA4ODg0NzQzMS0zZWo5M3F1Mm9sYms1bWJoaG1pamwyYjlpNWY5Nmw4ay5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExMzEyNTAzMTY1OTQ4OTI5Mjg4NSIsImVtYWlsIjoiamp1bjk0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoianVueWVvbmcgY2hvaSIsInBpY3R1cmUiOiJodHRwczovL2xoNi5nb29nbGV1c2VyY29udGVudC5jb20vLUtucTRFVVNuWTVVL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FBS1dKSk9INzV1TEFVWVhnMkRGWWFoT2thZFBKVGpVUGcvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6Imp1bnllb25nIiwiZmFtaWx5X25hbWUiOiJjaG9pIiwibG9jYWxlIjoia28iLCJpYXQiOjE1ODU4MTM1NTksImV4cCI6MTU4NTgxNzE1OX0.f4OnZu0EoUrX24qG4PuahP2Eyaz3H957tA586BLv_gD5xXlERdqQLLbJyD3-gH0Dd24r-RErsU9zxKOa86YXHsAHLdtmlLZ4LJrOyp1EiEQFTdUqvYdFEbtxCFWRz0F2Grcntun2Pj9md_odddemTgzEaE1OWKxnJRqe_3eD9P6EjY380wvwveP8wZZqLW6LKg9fR8sPVwqZ_sYhlGvVWpqworLLibTrG55D_-KsN_DfLzSuPLXAQuWAjCBfvzTc9p-EICiroMgAvBVDeRsH98uM0c9iT42gqXGNBM2bhcfUMAuWOKDwRFU3k0GYYlKiYwJnofdY2nyKMFAunwe6XQ'

        params = {
            "token": token + '1',
        }
        response = self.client.post('/api/v1/user/google/sign-up/', params, format='json')
        pprint(response.json())

        self.assertEqual(response.status_code, 401)

        params = {
            "token": token,
        }
        self.client.post('/api/v1/user/google/sign-up/', params, format='json')
        params = {
            "token": token,
        }
        response = self.client.post('/api/v1/user/google/sign-up/', params, format='json')
        pprint(response.json())

        self.assertEqual(response.status_code, 400)

    def test_success_google_sign_in(self):
        '''
        google 로그인 성공 케이스
        '''
        token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1N2Y2YTU4MjhkMWU0YTNhNmEwM2ZjZDFhMjQ2MWRiOTU5M2U2MjQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDAyMDg4ODQ3NDMxLWo1azRsNXRhbGpoZjhycGVuYWpybHFnMWgxMTg3ZHI1LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTAwMjA4ODg0NzQzMS0zZWo5M3F1Mm9sYms1bWJoaG1pamwyYjlpNWY5Nmw4ay5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExMzEyNTAzMTY1OTQ4OTI5Mjg4NSIsImVtYWlsIjoiamp1bjk0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoianVueWVvbmcgY2hvaSIsInBpY3R1cmUiOiJodHRwczovL2xoNi5nb29nbGV1c2VyY29udGVudC5jb20vLUtucTRFVVNuWTVVL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FBS1dKSk9INzV1TEFVWVhnMkRGWWFoT2thZFBKVGpVUGcvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6Imp1bnllb25nIiwiZmFtaWx5X25hbWUiOiJjaG9pIiwibG9jYWxlIjoia28iLCJpYXQiOjE1ODU4MTM1NTksImV4cCI6MTU4NTgxNzE1OX0.f4OnZu0EoUrX24qG4PuahP2Eyaz3H957tA586BLv_gD5xXlERdqQLLbJyD3-gH0Dd24r-RErsU9zxKOa86YXHsAHLdtmlLZ4LJrOyp1EiEQFTdUqvYdFEbtxCFWRz0F2Grcntun2Pj9md_odddemTgzEaE1OWKxnJRqe_3eD9P6EjY380wvwveP8wZZqLW6LKg9fR8sPVwqZ_sYhlGvVWpqworLLibTrG55D_-KsN_DfLzSuPLXAQuWAjCBfvzTc9p-EICiroMgAvBVDeRsH98uM0c9iT42gqXGNBM2bhcfUMAuWOKDwRFU3k0GYYlKiYwJnofdY2nyKMFAunwe6XQ'

        params = {
            "token": token
        }
        response = self.client.post('/api/v1/user/google/sign-up/', params, format='json')
        response = self.client.post('/api/v1/user/google/sign-in/', params, format='json')
        pprint(response.json())

        self.assertEqual(response.status_code, 200)

    def test_fail_google_sign_in(self):
        '''
        google 로그인 실패 케이스
        1) 토큰이 유효하지않음
        2) 유저가 없음
        '''
        token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1N2Y2YTU4MjhkMWU0YTNhNmEwM2ZjZDFhMjQ2MWRiOTU5M2U2MjQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDAyMDg4ODQ3NDMxLWo1azRsNXRhbGpoZjhycGVuYWpybHFnMWgxMTg3ZHI1LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTAwMjA4ODg0NzQzMS0zZWo5M3F1Mm9sYms1bWJoaG1pamwyYjlpNWY5Nmw4ay5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExMzEyNTAzMTY1OTQ4OTI5Mjg4NSIsImVtYWlsIjoiamp1bjk0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoianVueWVvbmcgY2hvaSIsInBpY3R1cmUiOiJodHRwczovL2xoNi5nb29nbGV1c2VyY29udGVudC5jb20vLUtucTRFVVNuWTVVL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FBS1dKSk9INzV1TEFVWVhnMkRGWWFoT2thZFBKVGpVUGcvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6Imp1bnllb25nIiwiZmFtaWx5X25hbWUiOiJjaG9pIiwibG9jYWxlIjoia28iLCJpYXQiOjE1ODU4MTM1NTksImV4cCI6MTU4NTgxNzE1OX0.f4OnZu0EoUrX24qG4PuahP2Eyaz3H957tA586BLv_gD5xXlERdqQLLbJyD3-gH0Dd24r-RErsU9zxKOa86YXHsAHLdtmlLZ4LJrOyp1EiEQFTdUqvYdFEbtxCFWRz0F2Grcntun2Pj9md_odddemTgzEaE1OWKxnJRqe_3eD9P6EjY380wvwveP8wZZqLW6LKg9fR8sPVwqZ_sYhlGvVWpqworLLibTrG55D_-KsN_DfLzSuPLXAQuWAjCBfvzTc9p-EICiroMgAvBVDeRsH98uM0c9iT42gqXGNBM2bhcfUMAuWOKDwRFU3k0GYYlKiYwJnofdY2nyKMFAunwe6XQ'

        params = {
            "token": token
        }
        # response = self.client.post('/api/v1/user/google/sign-up/', params, format='json')
        # params = {
        #     "token": token+'1'
        # }
        # response = self.client.post('/api/v1/user/google/sign-in/', params, format='json')
        # pprint(response.json())
        # self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/v1/user/google/sign-in/', params, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 404)

    def test_obtain_jwt(self):
        '''
        토큰 얻는 테스트
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        pprint(response.json())
        jwt_token = response.json()['token']['access']

        response = self.client.post('/api/v1/user/token/', params, format='json')
        pprint(response.json())

    def test_verify_jwt(self):
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        jwt_token = response.json()['token']['access']
        token = {
            'token': jwt_token
        }
        response = self.client.post('/api/v1/user/token/verify/', token, format='json')
        print(response.json())
        self.assertEqual(token['token'], response.json()['token'])

    def test_refresh_jwt(self):
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        access_token = response.json()['token']['access']
        refresh_token = response.json()['token']['refresh']
        token = {
            'refresh': refresh_token
        }
        response = self.client.post('/api/v1/user/token/refresh/', token, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 200)

    def test_fail_refresh_jwt(self):
        '''
        Refresh 토큰 실패 케이스
        1) 이미 블랙 리스트된 리프레시 토큰임
        2) 만료된 리프레시 토큰임
        '''
        params = {
            "email": "test@naver.com",
            "password": "123123",
            "username": "123123"
        }
        response = self.client.post('/api/v1/user/sign-up/', params, format='json')
        access_token = response.json()['token']['access']
        refresh_token = response.json()['token']['refresh']

        params = {
            "refresh": refresh_token
        }
        response = self.client.post('/api/v1/user/sign-out/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {access_token}'})
        pprint(response.json())
        token = {
            'refresh': refresh_token
        }
        response = self.client.post('/api/v1/user/token/refresh/', token, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 401)

        # ------------------------------------------------------------------------------------------------------
        sleep(2)
        token = {
            'refresh': refresh_token
        }
        response = self.client.post('/api/v1/user/token/refresh/', token, format='json')
        pprint(response.json())
        self.assertEqual(response.status_code, 401)
