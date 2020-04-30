from server.models.category import Category

from django.conf import settings
from django.db import models

from rest_framework import serializers


class Url(models.Model):

    url = models.CharField(max_length=300)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='urls', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='urls', on_delete=models.CASCADE)


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'
