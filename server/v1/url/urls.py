from django.urls import path

from .views import UrlListCreateAPIView, UrlDestroyAPIView

app_name = 'url'
urlpatterns = [
    path('', UrlListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', UrlDestroyAPIView.as_view(), name='delete'),
]
