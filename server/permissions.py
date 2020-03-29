from rest_framework import permissions

from server.models.token import BlackListedToken


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsObjectMe(permissions.BasePermission):
    message = '해당 토큰으로 참조할 수 없습니다.'

    # def has_permission(self, request, view):
    #     return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsNotBlacklistedToken(permissions.BasePermission):
    message = '이미 logout 된 토큰입니다.'

    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            is_black_listed = BlackListedToken.objects.get(token=token)
            if is_black_listed:
                return False
        except BlackListedToken.DoesNotExist:
            return True
        return True
