from datetime import datetime, timezone, timedelta

from django.conf import settings
from django.db import models
from rest_framework import serializers

from server.exceptions import ServerException
from server.models.category import Category
from server.models.url import Url


class Alarm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='alarms', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='alarms', on_delete=models.CASCADE)
    url = models.ForeignKey(Url, related_name='alarms', on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    has_been_sent = models.BooleanField(default=False)
    has_done = models.BooleanField(default=False)
    has_read = models.BooleanField(default=False)
    reserved_time = models.DateTimeField(help_text='The time you want the status to change')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ["reserved_time"]


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'

    def create(self, validated_data):
        current_time = datetime.now(timezone(timedelta(hours=9)))
        if validated_data['reserved_time'] < current_time:
            raise ServerException('예약시간이 올바르지 않습니다.')
        return super().create(validated_data)
