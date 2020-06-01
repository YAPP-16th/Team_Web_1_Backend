from django.contrib import admin
from django.contrib.auth import get_user_model

from server.models.alarm import Alarm
from server.models.category import Category
from server.models.url import Url

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('sign_up_type', 'email', 'username', 'is_superuser', 'date_joined')


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Url)
admin.site.register(Alarm)
