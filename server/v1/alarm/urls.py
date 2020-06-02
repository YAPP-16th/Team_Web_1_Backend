from django.urls import path

from .views import AlarmListCreateAPIView, AlarmDestroyAPIView

app_name = 'alarm'
urlpatterns = [
    path('', AlarmListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', AlarmDestroyAPIView.as_view(), name='delete'),
]
