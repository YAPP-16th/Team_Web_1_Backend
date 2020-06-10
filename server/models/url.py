from django.conf import settings
from django.db import models
from django_filters import rest_framework as rest_framework_filters
from rest_framework import serializers

from server.models.category import Category


class Url(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='urls', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='urls', on_delete=models.CASCADE)
    path = models.CharField(max_length=500)
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=100, null=True)
    favicon_path = models.CharField(max_length=500)
    image_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ["-created_at"]


class UrlSerializer(serializers.ModelSerializer):
    has_alarms = serializers.SerializerMethodField()

    class Meta:
        model = Url
        fields = '__all__'

    def get_has_alarms(self, url):
        return url.alarms.exists()


class UrlFilter(rest_framework_filters.FilterSet):
    path = rest_framework_filters.CharFilter(field_name='path', lookup_expr='contains')
    title = rest_framework_filters.CharFilter(field_name='title', lookup_expr='contains')

    class Meta:
        model = Url
        fields = ['path', 'title']
