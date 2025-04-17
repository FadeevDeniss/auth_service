from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import UserProfile


class UserAdminBase(UserAdmin):
    model = UserProfile
    list_display = ['email']


admin.site.register(UserProfile, UserAdminBase)

