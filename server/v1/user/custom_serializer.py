from rest_framework_jwt.serializers import (JSONWebTokenSerializer, VerifyJSONWebTokenSerializer,
                                            RefreshJSONWebTokenSerializer)


class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):
    """
    Override rest_framework_jwt's ObtainJSONWebToken serializer to
    force it to raise ValidationError exception if validation fails.
    """

    def is_valid(self, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)


class CustomVerifyJSONWebTokenSerializer(VerifyJSONWebTokenSerializer):
    """
    Override rest_framework_jwt's VerifyJSONWebToken serializer to
    force it to raise ValidationError exception if validation fails.
    """

    def is_valid(self, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)


class CustomRefreshJSONWebTokenSerializer(RefreshJSONWebTokenSerializer):
    """
    Override rest_framework_jwt's VerifyJSONWebToken serializer to
    force it to raise ValidationError exception if validation fails.
    """

    def is_valid(self, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)
