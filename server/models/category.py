from django.conf import settings
from django.db import models
from rest_framework import serializers


class CustomCategoryManager(models.Manager):
    def get_my_last_order(self, request):
        my_categories = self.filter(user=request.user)
        if my_categories:
            return max([category.order for category in my_categories])
        return 0

    def move(self, obj, new_order):
        pass


class Category(models.Model):
    # TODO 메타정보 크롤러 있어야한다. url 앱에
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    is_favorited = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomCategoryManager()

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ["is_favorited", "order"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
