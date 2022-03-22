from django.contrib import admin

from accounts.models import SocialAccount


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ("provider", "unique_id", "line_id", "user")
    search_fields = ("line_id",)
