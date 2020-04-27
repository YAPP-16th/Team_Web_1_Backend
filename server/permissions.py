import requests
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = '해당 토큰으로 참조할 수 없습니다.'

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class IsObjectMe(permissions.BasePermission):
    message = '해당 토큰으로 참조할 수 없습니다.'

    # def has_permission(self, request, view):
    #     return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class GoogleAccessToken:
    def __init__(self, token):
        self.token = token

    def is_valid(self):
        # https://developers.google.com/identity/sign-in/web/backend-auth
        payload = {'id_token': self.token}  # validate the token
        response = requests.get('https://oauth2.googleapis.com/tokeninfo', params=payload)
        response = response.json()

        if 'error' in response or 'email' not in response:
            return False
        return response
