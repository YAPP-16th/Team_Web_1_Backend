from random import randint

import requests
from django.conf import settings
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
        # https://developers.google.com/people/api/rest/v1/people/get
        # https://developer.chrome.com/apps/identity
        people_api_url = 'https://people.googleapis.com/v1/people/me'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {self.token}',
        }
        payload = {
            'personFields': 'names,emailAddresses',
            'key': settings.GOOGLE_API_KEY
        }
        response = requests.get(people_api_url, params=payload, headers=headers)
        response = response.json()

        if 'error' in response or 'emailAddresses' not in response or \
                not response['emailAddresses'][0] or response['emailAddresses'][0].get('value') is None:
            return False

        return {
            'email': response['emailAddresses'][0]['value'],
            'username': response['names'][0].get('displayName', f'User{randint(1000, 99999)}')
        }
