from django.conf import settings
from django.db import models, transaction
from django.db.models import F
from rest_framework import serializers

from server.exceptions import ServerException


class CustomCategoryManager(models.Manager):
    def get_my_last_order(self, user):
        my_categories = self.filter(user=user)
        if my_categories:
            return my_categories.order_by('order').last().order
        return 0

    def move(self, instance, new_order):
        queryset = self.get_queryset()
        user = instance.user

        if new_order < 1 or self.get_my_last_order(user) < new_order:
            raise ServerException("잘못된 order 입니다.")

        with transaction.atomic():
            if instance.order > new_order:
                queryset.filter(
                    user=user,
                    order__lt=instance.order,
                    order__gte=new_order
                    # ).exclude(
                    #     pk=obj.pk
                ).update(
                    order=F('order') + 1
                )
            else:
                queryset.filter(
                    user=user,
                    order__lte=new_order,
                    order__gt=instance.order
                    # ).exclude(
                    #     pk=obj.pk
                ).update(
                    order=F('order') - 1
                )
            instance.order = new_order
            instance.save()
        return instance


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
        ordering = ["-is_favorited", "order"]


class CategorySerializer(serializers.ModelSerializer):
    url_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def update(self, instance, validated_data):
        order = validated_data.pop('order', None)
        if isinstance(order, int) and instance.order != order:
            Category.objects.move(instance, order)
        return super().update(instance, validated_data)

    def get_url_count(self, category):
        return category.urls.count()

    def create(self, validated_data):
        instance = super().create(validated_data)
        if instance.order != 1:
            return Category.objects.move(instance, 1)
        return instance
