import random
import string

import requests
from django.contrib.auth import login, logout
from rest_framework import generics, status, views
from rest_framework.response import Response

from server.models.user import User, UserSerializer, UserSignInSerializer
from server.permissions import IsAuthenticatedAndOwner


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedAndOwner, ]


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
    def post(self, request):
        logout(self.request)
        return Response({'logout': True})


class GoogleSignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

    def make_random_string_for_password(self):
        string_pool = string.ascii_letters + string.digits
        return ''.join([random.choice(string_pool) for i in range(12)])

    def post(self, request, *args, **kwargs):
        payload = {'access_token': request.data.get("token")}  # validate the token
        # https://developers.google.com/identity/sign-in/web/backend-auth
        # https: // oauth2.googleapis.com / tokeninfo
        response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        response = response.json()

        if 'error' in response:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        request.data = {
            'username': response['email'].split('@')[0],
            'email': response['email'],
            'password': self.make_random_string_for_password()
        }
        self.create(self, request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)


class GoogleSignInView(views.APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        # https://developers.google.com/identity/sign-in/web/backend-auth
        # https: // oauth2.googleapis.com / tokeninfo
        response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        response = response.json()

        if 'error' in response:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(email=response['email'])
            login(self.request, user)
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
