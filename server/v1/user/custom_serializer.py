from rest_framework_simplejwt import serializers


class CustomTokenVerifySerializer(serializers.TokenVerifySerializer):
    def validate(self, attrs):
        from rest_framework_simplejwt.tokens import UntypedToken
        UntypedToken(attrs['token'])

        return {'token': attrs['token'],
                'message': '유효한 토큰입니다.',
                'status_code': 200}
