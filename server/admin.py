from django.contrib import admin
from django.contrib.auth import get_user_model

from server.models.category import Category
from server.models.url import Url
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'password', 'username', 'is_superuser', 'date_joined')


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Url)
