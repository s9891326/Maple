from django.contrib import admin

from coins.models import Coin


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ("title", "value", "total",)
    search_fields = ("title",)
    ordering = ("create_date",)
