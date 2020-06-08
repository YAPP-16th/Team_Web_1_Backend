from datetime import datetime, timedelta

from django.test import TestCase
from rest_framework.test import APIClient


class AlarmTest(TestCase):
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

        params = {
            "path": [
                "https://www.lfmall.co.kr/product.do?cmd=getProductDetail&PROD_CD=TGTS0B705WT&etag1=108_A011_E043&etag2=0&etag3=2&etag4=1004"]
        }

        response = self.client.post(f'/api/v1/url/?category={self.category_id}', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.url_id = response.json()[0]['id']

        self.tomorrow = datetime.now() + timedelta(days=1)

    def test_success_alarm_create(self):
        params = {
            "name": '알람 테스트',
            'reserved_time': {"year": self.tomorrow.year,
                              "month": self.tomorrow.month,
                              "day": self.tomorrow.day,
                              "hour": self.tomorrow.hour,
                              "minute": self.tomorrow.minute}
        }

        response = self.client.post(f'/api/v1/alarm/?category={self.category_id}&url={self.url_id}', params,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['id'], 1)

        params = {
            "name": '알람 테스트',
            'reserved_time': {"year": self.tomorrow.year,
                              "month": self.tomorrow.month,
                              "day": self.tomorrow.day,
                              "hour": self.tomorrow.hour,
                              "minute": self.tomorrow.minute}
        }

        response = self.client.post(f'/api/v1/alarm/?category={self.category_id}&url={self.url_id}', params,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['id'], 2)

    def test_fail_alarm_create(self):
        '''
        실패 케이스
        1. 현재시간보다 이전 시간을 예약한다.
        2. 시간 형식이 올바르지 않다.
        3. 필드가 빠져있다.
        4. 시간 딕셔너리가 올바르지 않다.
        '''

        # 현재시간보다 이전 시간
        params = {
            "name": '알람 테스트',
            'reserved_time': {"year": "2020", "month": "06", "day": "1", "hour": "20", "minute": "28"}
        }

        response = self.client.post(f'/api/v1/alarm/?category={self.category_id}&url={self.url_id}', params,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 500)

        # 시간 형식이 올바르지 않다
        params = {
            "name": '알람 테스트',
            'reserved_time': {"year": "20201", "month": "06", "day": "1", "hour": "20", "minute": "28"}
        }

        response = self.client.post(f'/api/v1/alarm/?category={self.category_id}&url={self.url_id}', params,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 500)

        # 필드가 빠져있다.
        params = {
            'reserved_time': {"year": "2020", "month": "06", "day": "1", "hour": "20", "minute": "28"}
        }

        response = self.client.post(f'/api/v1/alarm/?category={self.category_id}&url={self.url_id}', params,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 400)

        # 시간 딕셔너리가 올바르지 않다.
        params = {
            "name": '알람 테스트',
            'reserved_time': {"yeara": "2020"}
        }

        response = self.client.post(f'/api/v1/alarm/?category={self.category_id}&url={self.url_id}', params,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 500)

    def test_success_delete_alarm(self):
        params = {
            "name": '알람 테스트',
            'reserved_time': {"year": self.tomorrow.year,
                              "month": self.tomorrow.month,
                              "day": self.tomorrow.day,
                              "hour": self.tomorrow.hour,
                              "minute": self.tomorrow.minute}
        }

        response = self.client.post(f'/api/v1/alarm/?category={self.category_id}&url={self.url_id}', params,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 201)

        response = self.client.delete(f'/api/v1/alarm/{response.json()["id"]}/',
                                      **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'/api/v1/alarm/1/',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 405)

    def test_fail_delete_alarm(self):
        '''
        실패 케이스
        1. 없는 id를 삭제
        2. 남의 알람을 삭제
        '''
        params = {
            "name": '알람 테스트',
            'reserved_time': {"year": self.tomorrow.year,
                              "month": self.tomorrow.month,
                              "day": self.tomorrow.day,
                              "hour": self.tomorrow.hour,
                              "minute": self.tomorrow.minute}
        }

        response = self.client.post(f'/api/v1/alarm/?category={self.category_id}&url={self.url_id}', params,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 201)

        response = self.client.post(f'/api/v1/alarm/?category={self.category_id}&url={self.url_id}', params,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})
        self.assertEqual(response.status_code, 201)

        # 없는 id를 삭제
        response = self.client.delete(f'/api/v1/alarm/3/',
                                      **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 404)

        # 남의 알람을 삭제
        response = self.client.delete(f'/api/v1/alarm/2/',
                                      **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 403)

    def test_fail_other_method_alarm(self):
        '''
        get, put, patch로 요청했을 경우 에러 반환
        '''
        params = {
            "name": '알람 테스트',
            'reserved_time': {"year": "2020", "month": "06", "day": "2", "hour": "20", "minute": "28"}
        }

        response = self.client.get(f'/api/v1/alarm/1/',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 405)

        response = self.client.put(f'/api/v1/alarm/1/', params, format='json',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(f'/api/v1/alarm/1/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 405)
