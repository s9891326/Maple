from django.contrib import admin
from exchange.models import EquipLibrary, Equip


class EquipLibraryAdmin(admin.ModelAdmin):
    list_display = ("category", "type", "name")
    search_fields = ("name",)


admin.site.register(EquipLibrary, EquipLibraryAdmin)


class EquipAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Equip, EquipAdmin)
