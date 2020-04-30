from django.urls import path

from .views import AlarmListCreateAPIView, AlarmRetrieveUpdateDestroyAPIView

app_name = 'alarm'
urlpatterns = [
    path('', AlarmListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', AlarmRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
]
