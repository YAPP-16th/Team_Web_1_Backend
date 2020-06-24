from django.urls import path

from .views import UrlListCreateAPIView, UrlRetrieveUpdateDestroyAPIView

app_name = 'url'
urlpatterns = [
    path('', UrlListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', UrlRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
]
