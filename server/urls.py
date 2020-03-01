from django.urls import path, include

app_name = 'server'
urlpatterns = [
    path('v1/', include('server.v1.urls', namespace='v1')),
]