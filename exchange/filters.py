import django_filters

from exchange.models import ProductList, Product


class ProductListFilter(django_filters.FilterSet):
    # star = django_filters.NumberFilter(field_name="product__star", lookup_expr="gte")
    
    class Meta:
        model = ProductList
        fields = ('category', 'type', 'stage_level', 'name')


class ProductFilter(django_filters.FilterSet):
    product_list_id = django_filters.NumberFilter(field_name="product_list", required=True)
    star = django_filters.NumberFilter(field_name="star", lookup_expr="gte")
    total_level = django_filters.NumberFilter(field_name="total_level", lookup_expr="gte")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    label_level = django_filters.AllValuesMultipleFilter(field_name="label_level")
    
    class Meta:
        model = Product
        fields = ('is_maple', 'maple_capability', 'total_level')
