import random
import string

from django.contrib.auth import login, logout
from rest_framework import generics, status, views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken, RefreshJSONWebToken

from server.models.token import BlackListedToken
from server.models.user import User, UserSerializer, UserSignInSerializer
from server.permissions import IsObjectMe, IsNotBlacklistedToken, GoogleAccessToken
from server.v1.user.custom_serializer import (CustomJSONWebTokenSerializer, CustomVerifyJSONWebTokenSerializer,
                                              CustomRefreshJSONWebTokenSerializer)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    # TODO 현재 email도 수정할 수 있는데 serializer를 분리해서 email 필드는 수정불가하도록해야함.
    """
        ## `JWT 필요`
        ## Headers
            - Authorization : JWT <토큰>
        ## Path Params
            - id : 유저 id(이메일주소 X)
        ## Body(UPDATE 요청 시)
            - username : 유저네임
            - password : 패스워드(6자리 이상)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectMe]


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

        ---
        ## `JWT 필요`
        ## Headers
            - Authorization : JWT <토큰>
    """
    permission_classes = [permissions.IsAuthenticated, IsNotBlacklistedToken]

    def post(self, request):
        logout(self.request)
        token = request.META.get('HTTP_AUTHORIZATION')
        BlackListedToken.objects.create(token=token)
        return Response({'logout': True})


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
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        user_email = response['email']
        request.data['username'] = response.get('name', user_email.split('@')[0])
        request.data['email'] = user_email
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


class CustomObtainJSONWebToken(ObtainJSONWebToken):
    """
        JWT 발급 API

        ## 주의사항
            1) 발급 or 갱신 후 7일 안에는 (재)갱신 가능
                - 7일 후에는 (재)갱신 불가능
            2) 발급 or 갱신 후 28일 후에는 재갱신 불가능
                - 7일 안에 계속 갱신이 이루어져도 28일 후에는 불가능
            3) 만료 시 /user/token/ 으로 email, password 와 함께 재발급
        ---
        ## `JWT 불필요`
        ## Headers
            - Content type : application/json
        ## Body
            - email : 이메일
            - password : 패스워드(6자리 이상)
    """
    serializer_class = CustomJSONWebTokenSerializer


class CustomVerifyJSONWebToken(VerifyJSONWebToken):
    """
        JWT 검증 API

        ---
        ## `JWT 불필요`
        ## Headers
            - Content type : application/json
        ## Body
            - token : <JWT 토큰>
    """
    serializer_class = CustomVerifyJSONWebTokenSerializer


class CustomRefreshJSONWebToken(RefreshJSONWebToken):
    """
        JWT 갱신 API

        ---
        ## `JWT 불필요`
        ## Headers
            - Content type : application/json
        ## Body
            - token : <JWT 토큰>
    """
    serializer_class = CustomRefreshJSONWebTokenSerializer
