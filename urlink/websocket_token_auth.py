from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken


@database_sync_to_async
def get_user(user_id):
    return get_user_model().objects.get(id=user_id)


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    see:
    https://channels.readthedocs.io/en/latest/topics/authentication.html#custom-authentication
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(self, scope)


class TokenAuthMiddlewareInstance:
    def __init__(self, middleware, scope):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        token = parse_qs(self.scope["query_string"].decode("utf8")).get('token')
        if token:
            token = token[0]
            try:
                UntypedToken(token)
            except (InvalidToken, TokenError) as e:
                print(e)
                return None
            else:
                decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = await get_user(decoded_data['user_id'])
                if user.is_authenticated:
                    self.scope['user'] = user
                    inner = self.inner(self.scope)
                    return await inner(receive, send)
