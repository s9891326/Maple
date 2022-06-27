from django.contrib import admin

from coins.models import Coin


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ("title", "value", "total", "pay_method", "contact_method")
    list_filter = ("pay_method", "contact_method")
    search_fields = ("title", "pay_method",)
    ordering = ("create_date",)
