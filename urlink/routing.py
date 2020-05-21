from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from server.v1.alarm.channels.router import websocket_urlpatterns
from .websocket_token_auth import TokenAuthMiddleware

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))

application = ProtocolTypeRouter({
    # http->django views is added by default
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
