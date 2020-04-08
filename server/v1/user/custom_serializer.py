from rest_framework_jwt.serializers import (JSONWebTokenSerializer, VerifyJSONWebTokenSerializer,
                                            RefreshJSONWebTokenSerializer)


class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):

    def is_valid(self, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)


class CustomVerifyJSONWebTokenSerializer(VerifyJSONWebTokenSerializer):

    def is_valid(self, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)


class CustomRefreshJSONWebTokenSerializer(RefreshJSONWebTokenSerializer):

    def is_valid(self, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)
