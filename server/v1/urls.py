from django.urls import path, include

app_name = 'v1'
urlpatterns = [
    path('user/', include('server.v1.user.urls', namespace='user')),
    path('category/', include('server.v1.category.urls', namespace='category')),
    path('url/', include('server.v1.url.urls', namespace='url')),
    path('alarm/', include('server.v1.alarm.urls', namespace='alarm')),
]
