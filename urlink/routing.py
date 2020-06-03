from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from server.v1.alarm.channels.consumer import AlarmConsumer
from .websocket_token_auth import TokenAuthMiddleware

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))

application = ProtocolTypeRouter({
    # http->django views is added by default
    'websocket': TokenAuthMiddlewareStack(
        URLRouter([
            path('ws/connection/', AlarmConsumer)
        ])
    ),
})
