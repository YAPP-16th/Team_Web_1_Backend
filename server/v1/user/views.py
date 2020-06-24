import random
import string

from django.contrib.auth import login, logout
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from server.exceptions import ServerException
from server.models.user import User, UserSerializer, UserSignInSerializer
from server.permissions import GoogleAccessToken
from server.v1.user.custom_serializer import CustomTokenVerifySerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        ## `JWT 필요`
        ## Headers
            - Authorization : JWT <토큰>
        ## Body(UPDATE 요청 시)
            - username : 유저네임
            - password : 패스워드(6자리 이상)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SignUpView(generics.CreateAPIView):
    """
        일반 회원가입 API

        ---
        ## `JWT 불필요`
        ## Headers
            - Content type : application/json
        ## Body
            - email : 이메일
            - username : 유저네임
            - password : 패스워드(6자리 이상)
    """
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)


class SignInView(views.APIView):
    """
        일반 로그인 API

        ---
        ## `JWT 불필요`
        ## Headers
            - Content type : application/json
        ## Body
            - email : 이메일
            - password : 패스워드(6자리 이상)
    """
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(self.request, user)
        return Response(UserSerializer(user).data)


class SignoutView(views.APIView):
    """
        일반 로그아웃 API

        - 해당 Refresh 토큰 무효화
        ---
        ## `JWT 필요`
        ## Headers
            - Authorization : JWT <토큰>
        ## Body
            - refresh : Refresh 토큰
    """

    def post(self, request):
        refresh_token = request.data.get('refresh')
        try:
            token = RefreshToken(refresh_token)
        except Exception:
            raise ServerException('유효하지 않은 Refresh 토큰입니다.')
        token.blacklist()
        logout(self.request)
        return Response({'logout': True, 'message': '해당 Refresh 토큰은 이제 사용할 수 없습니다.'})


class GoogleSignUpView(generics.CreateAPIView):
    """
        구글 회원가입 API

        ---
        ## `JWT 불필요`
        ## `email, username, password 불필요`
        ## Headers
            - Content type : application/json
        ## Body
            - token : 구글 access token
    """
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

    def make_random_string_for_password(self):
        string_pool = string.ascii_letters + string.digits
        return ''.join([random.choice(string_pool) for i in range(26)])

    def post(self, request, *args, **kwargs):
        response = GoogleAccessToken(request.data.get("token")).is_valid()
        if not response:
            content = {'message': '유효하지 않은 토큰 혹은 email 정보를 가져올 수 없습니다.'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        request.data['username'] = response['username']
        request.data['email'] = response['email']
        request.data['password'] = self.make_random_string_for_password()
        request.data['sign_up_type'] = 'google'
        request.data.pop('token', None)

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)


class GoogleSignInView(views.APIView):
    """
        구글 로그인 API

        ---
        ## `JWT 불필요`
        ## `email, password 불필요`
        ## Headers
            - Content type : application/json
        ## Body
            - token : 구글 access token
    """
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        response = GoogleAccessToken(request.data.get("token")).is_valid()
        if not response:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(email=response['email'])
            login(self.request, user)
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            content = {'message': '해당 User는 존재하지 않습니다.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class CustomObtainJSONWebToken(TokenObtainPairView):
    """
        JWT 발급 API

        ## 주의사항
            1) Access Token 유효기간 2시간
            2) Refresh Token 유효기간 30일
            3) Access Token 만료 시
                - url : /user/token/refresh/
                - body : {refresh: Refresh 토큰} 으로 Access Token 재발급
            4) Refresh Token 만료 시
                - /user/sign-in/ 으로 재 로그인
                - 혹은 /user/token/ 으로 email, password 와 함께 재발급
        ---
        ## `JWT 불필요`
        ## Headers
            - Content type : application/json
        ## Body
            - email : 이메일
            - password : 패스워드(6자리 이상)
    """
    pass


class CustomVerifyJSONWebToken(TokenVerifyView):
    """
        JWT 검증 API

        ---
        ## `JWT 불필요`
        ## Headers
            - Content type : application/json
        ## Body
            - token : <JWT Access Token or Refresh Token>
    """
    serializer_class = CustomTokenVerifySerializer


class CustomRefreshJSONWebToken(TokenRefreshView):
    """
        JWT 갱신 API

        ---
        ## `JWT 불필요`
        ## Headers
            - Content type : application/json
        ## Body
            - refresh : <JWT Refresh Token>
    """
    pass
