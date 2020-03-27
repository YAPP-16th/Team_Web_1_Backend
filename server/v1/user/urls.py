from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .views import UserDetail, SignUpView, SignInView, SignoutView, GoogleSignUpView, GoogleSignInView

app_name = 'user'
urlpatterns = [
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),

    path('google/sign-up/', GoogleSignUpView.as_view(), name='google_sign_up'),
    path('google/sign-in/', GoogleSignInView.as_view(), name='google_sign_in'),

    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    path('sign-out/', SignoutView.as_view(), name='sign_out'),

    path('token/', obtain_jwt_token),  # JWT 토큰 획득
    path('token/refresh/', refresh_jwt_token),  # JWT 토큰 갱신
    path('token/verify/', verify_jwt_token),  # JWT 토큰 확인
]
