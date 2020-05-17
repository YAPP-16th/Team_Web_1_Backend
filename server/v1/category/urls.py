from django.urls import path

from .views import CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView

app_name = 'category'
urlpatterns = [
    path('', CategoryListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
]