import random
import string

from django.contrib.auth import login, logout
from rest_framework import generics, status, views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken

from server.models.token import BlackListedToken
from server.models.user import User, UserSerializer, UserSignInSerializer
from server.permissions import IsObjectMe, IsNotBlacklistedToken, GoogleAccessToken
from .custom_serializer import JSONWebTokenSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectMe]
    # TODO 현재 email도 수정할 수 있는데 serializer를 분리해서 email 필드는 수정불가하도록해야함.


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)


class SignInView(views.APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(self.request, user)
        return Response(UserSerializer(user).data)


class SignoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotBlacklistedToken]

    def post(self, request):
        '''
        로그아웃하면 해당토큰을 blacklisted token db에 넣어서 다시 사용할 수 없게 만든다.
        '''
        logout(self.request)
        token = request.META.get('HTTP_AUTHORIZATION')
        BlackListedToken.objects.create(token=token)
        return Response({'logout': True})


class GoogleSignUpView(generics.CreateAPIView):
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


# class CustomObtainJSONWebToken(ObtainJSONWebToken):
#     """
#     Override the default JWT ObtainJSONWebToken view to use the custom serializer
#     """
#     serializer_class = JSONWebTokenSerializer
