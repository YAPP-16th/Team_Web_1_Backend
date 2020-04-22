from django.db import models
from server.models.category import Category
from server.models.user import User
from django.conf import settings
from django.db import models, transaction
from django.db.models import F
from rest_framework import serializers
from server.exceptions import ServerException

class Url(models.Model):
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=350)
    image = models.CharField(max_length=350)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='url_users', on_delete=models.CASCADE)
    category = models.ForeignKey(settings.AUTH_CATEGORY_MODEL, related_name='url_categorys', on_delete=models.CASCADE)