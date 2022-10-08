from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'provider', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'provider', 'is_staff', 'is_active',)
    search_fields = ('username',)
    ordering = ('date_joined',)
