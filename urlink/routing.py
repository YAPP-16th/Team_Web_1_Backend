from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from server.v1.alarm.urls import urlpatterns as alarm_url_patterns

application = ProtocolTypeRouter({
    # http->django views is added by default
    'websocket': AuthMiddlewareStack(
        URLRouter(
            alarm_url_patterns
        )
    ),
})
