from django.conf import settings
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

app_name = 'server'
urlpatterns = [
    path('v1/', include('server.v1.urls', namespace='v1')),
]

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Urlink API",
            default_version='v1',
            description="Urlink API Docs",
        ),
        public=True,
        permission_classes=(),
    )
    schema_view()
    urlpatterns = [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ] + urlpatterns
