from django.urls import path

from .views import SignUpView

app_name = 'user'
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
]
