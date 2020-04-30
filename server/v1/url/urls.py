
from django.urls import path

from .views import UrlListCreateAPIView

app_name = 'url'
urlpatterns = [
    path('', UrlListCreateAPIView.as_view(), name='list_create'),
]

