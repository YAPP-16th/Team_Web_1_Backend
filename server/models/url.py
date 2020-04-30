from django.conf import settings
from django.db import models
from rest_framework import serializers

from server.models.category import Category


class Url(models.Model):
    path = models.CharField(max_length=500)
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=100)
    image_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='urls', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='urls', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ["-created_at"]


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'
