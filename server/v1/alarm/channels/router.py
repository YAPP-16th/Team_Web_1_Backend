from django.urls import path

from .consumer import Consumer

websocket_urlpatterns = [
    path('api/v1/ws/connection/', Consumer),
]
