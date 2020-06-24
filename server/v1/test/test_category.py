from pprint import pprint

from django.test import TestCase
from rest_framework.test import APIClient


class CategoryTest(TestCase):
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

    def test_success_category_create(self):
        params = {
            "name": "test"
        }
        for i in range(4):
            response = self.client.post('/api/v1/category/', params, format='json',
                                        **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

            self.assertEqual(response.status_code, 201)



        for i in range(4):
            response = self.client.post('/api/v1/category/', params, format='json',
                                        **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})

            self.assertEqual(response.status_code, 201)

    def test_fail_category_create(self):
        '''
        카테고리 생성 실패 케이스
        1) 잘못된 토큰으로 생성
        '''
        params = {
            "name": "test"
        }
        response = self.client.post('/api/v1/category/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}1'})

        self.assertEqual(response.status_code, 401)

    def test_success_category_list(self):
        params = {
            "name": "test"
        }
        for i in range(4):
            self.client.post('/api/v1/category/', params, format='json',
                             **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})

        self.assertEqual(response.status_code, 200)

    def test_fail_category_list(self):
        '''
        카테고리 리스트 조회 실패 케이스
        1) 잘못된 토큰으로 조회
        '''
        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}1'})

        self.assertEqual(response.status_code, 401)

    def test_success_category_get(self):
        params = {
            "name": "test"
        }
        response = self.client.post('/api/v1/category/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        category = response.json()['id']

        response2 = self.client.get(f'/api/v1/category/{category}/',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response.json(), response2.json())

    def test_fail_category_get(self):
        '''
        카테고리 디테일 조회 실패 케이스
        1) 없는 pk로 조회
        2) 권한이 없는 카테고리 조회
        '''
        params = {
            "name": "test"
        }

        # 없는 pk로 조회
        response = self.client.post('/api/v1/category/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        category = response.json()['id']
        response = self.client.get(f'/api/v1/category/{category + 1}/',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 404)

        # 권한이 없는 pk로 조회
        response = self.client.get(f'/api/v1/category/{category}/',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})

        self.assertEqual(response.status_code, 403)

    def test_success_category_delete(self):
        params = {
            "name": "test"
        }
        response = self.client.post('/api/v1/category/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        category = response.json()['id']
        response = self.client.delete(f'/api/v1/category/{category}/',
                                      **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 204)

        # 여러개를 만들고 1번 삭제하면 그 밑에 order들이 1씩 땡겨지는지 테스트
        for i in range(4):
            params = {
                "name": f"test{i}"
            }
            self.client.post('/api/v1/category/', params, format='json',
                             **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        response = self.client.delete(f'/api/v1/category/2/',
                                      **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})


    def test_fail_category_delete(self):
        '''
        카테고리 디테일 조회 실패 케이스
        1) 없는 pk로 삭제
        2) 권한이 없는 카테고리 삭제
        '''

        params = {
            "name": "test"
        }

        # 없는 pk로 삭제
        response = self.client.post('/api/v1/category/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        category = response.json()['id']
        response = self.client.delete(f'/api/v1/category/{category + 1}/',
                                      **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 404)

        # # 권한이 없는 pk로 삭제
        response = self.client.delete(f'/api/v1/category/{category}/',
                                      **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})

        self.assertEqual(response.status_code, 403)

    def test_success_category_update_put(self):
        params = {
            "name": "test"
        }

        response = self.client.post('/api/v1/category/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        category = response.json()['id']

        # 이름 변경
        params["name"] = "test123123"
        response = self.client.put(f'/api/v1/category/{category}/', params, format='json',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

        # favorite 변경
        params["is_favorited"] = "true"
        response = self.client.put(f'/api/v1/category/{category}/', params, format='json',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

    def test_fail_category_update_put(self):
        '''
        카테고리 put 방식 업데이트 실패 케이스
        1) 없는 pk로 업데이트
        2) 권한이 없는 카테고리 업데이트
        3) 필드 누락
        '''
        params = {
            "name": "test"
        }

        response = self.client.post('/api/v1/category/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        category = response.json()['id']

        # 없는 pk로 업데이트
        params["name"] = "test123123"
        response = self.client.put(f'/api/v1/category/{category + 1}/', params, format='json',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 404)

        # 권한이 없는 카테고리 업데이트
        response = self.client.put(f'/api/v1/category/{category}/', params, format='json',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})

        self.assertEqual(response.status_code, 403)

        # 필드 누락
        params = {
            "is_favorited": "true"
        }
        response = self.client.put(f'/api/v1/category/{category}/', params, format='json',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 400)

    def test_success_category_update_patch(self):
        params = {
            "name": "test"
        }

        response = self.client.post('/api/v1/category/', params, format='json',
                                    **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        category = response.json()['id']

        # 이름 변경
        params["name"] = "test123123"
        response = self.client.patch(f'/api/v1/category/{category}/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

        # favorite 변경
        params = {
            "is_favorited": "true"
        }
        response = self.client.patch(f'/api/v1/category/{category}/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

    def test_success_category_order_change(self):
        for i in range(50):
            params = {
                "name": f"test{i}"
            }
            self.client.post('/api/v1/category/', params, format='json',
                             **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        params = {
            "order": 3
        }
        response = self.client.patch(f'/api/v1/category/50/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['order'], 3)

        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})


        params = {
            "name": "느으으아아아앙",
            "order": 1
        }
        response = self.client.put(f'/api/v1/category/49/', params, format='json',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['order'], 1)

        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})


        params = {
            "is_favorited": "true"
        }
        response = self.client.patch(f'/api/v1/category/48/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})


    def test_fail_category_order_change(self):
        '''
        카테고리 순서 변경 실패 케이스
        1) 업데이트를 원하는 번호가 1보다 작다.
        2) 업데이트를 원하는 번호가 현재 최대 번호보다 크다.
        3) 필드 누락
        '''
        for i in range(1, 11):
            params = {
                "name": f"test{i}"
            }
            self.client.post('/api/v1/category/', params, format='json',
                             **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        # 업데이트를 원하는 번호가 1보다 작다.
        params = {
            "order": 0
        }
        response = self.client.patch(f'/api/v1/category/3/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 500)

        # 업데이트를 원하는 번호가 현재 최대 번호보다 크다.
        params = {
            "order": 11
        }
        response = self.client.patch(f'/api/v1/category/3/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 500)

        # 필드 누락
        params = {
            "order": 11
        }
        response = self.client.put(f'/api/v1/category/3/', params, format='json',
                                   **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 400)

    def test_category_list_order_by(self):
        for i in range(50):
            params = {
                "name": f"test{i}"
            }
            self.client.post('/api/v1/category/', params, format='json',
                             **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        params = {
            "order": 3
        }
        response = self.client.patch(f'/api/v1/category/50/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
        params = {
            "is_favorited": "true",
            "order": 2
        }
        response = self.client.patch(f'/api/v1/category/49/', params, format='json',
                                     **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['is_favorited'], True)

        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})


    def test_new_category_create(self):
        '''
        2020.05.29
        기존에는 카테고리를 추가할 시 가장 마지막 번호로 order가 정해졌는데
        새로추가되면 order는 1이되고 하위 order들이 1씩 밀리도록 수정
        '''
        for i in range(4):
            params = {
                "name": f"test_user_1_{i}"
            }
            response = self.client.post('/api/v1/category/', params, format='json',
                                        **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})
            self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token}'})

        self.assertEqual(response.status_code, 200)



        for i in range(4):
            params = {
                "name": f"test_user_2_{i}"
            }
            response = self.client.post('/api/v1/category/', params, format='json',
                                        **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})
            self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/category/', **{'HTTP_AUTHORIZATION': f'JWT {self.access_token2}'})

        self.assertEqual(response.status_code, 200)
