from django.contrib import admin
from exchange.models import ProductList, Product, ProductImage


@admin.register(ProductList)
class ProductListAdmin(admin.ModelAdmin):
    list_display = ("category", "type", "stage_level", "name")
    search_fields = ("name",)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_list", "star", "level", "total_level", "price", "update_date")
    search_fields = ("product_list",)
    inlines = (ProductImageInline,)
    ordering = ("product_list", "update_date")


admin.site.register(Product, ProductAdmin)
