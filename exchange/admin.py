from django.contrib import admin
from exchange.models import EquipLibrary, Equip, EquipImage

@admin.register(EquipLibrary)
class EquipLibraryAdmin(admin.ModelAdmin):
    list_display = ("category", "type", "stage_level", "name")
    search_fields = ("name",)


class EquipImageInline(admin.StackedInline):
    model = EquipImage
    extra = 1


# @admin.register(Equip)
class EquipAdmin(admin.ModelAdmin):
    list_display = ("equip_library",)
    search_fields = ("equip_library",)
    inlines = (EquipImageInline,)


admin.site.register(Equip, EquipAdmin)
