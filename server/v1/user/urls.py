from django.urls import path

from .views import (UserDetail, SignUpView, SignInView, SignoutView, GoogleSignUpView, GoogleSignInView,
                    CustomRefreshJSONWebToken, CustomVerifyJSONWebToken, CustomObtainJSONWebToken)

app_name = 'user'
urlpatterns = [
    path('', UserDetail.as_view(), name='user-detail'),

    path('google/sign-up/', GoogleSignUpView.as_view(), name='google_sign_up'),
    path('google/sign-in/', GoogleSignInView.as_view(), name='google_sign_in'),

    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    path('sign-out/', SignoutView.as_view(), name='sign_out'),

    path('token/', CustomObtainJSONWebToken.as_view(), name='obtain_json_web_token'),  # JWT 토큰 획득
    path('token/refresh/', CustomRefreshJSONWebToken.as_view(), name='refresh_json_web_token'),  # JWT 토큰 갱신
    path('token/verify/', CustomVerifyJSONWebToken.as_view(), name='verify_json_web_token'),  # JWT 토큰 확인
]
