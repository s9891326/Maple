from django.contrib import admin
from exchange.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    search_fields = ("name", "type")

admin.site.register(Category, CategoryAdmin)
