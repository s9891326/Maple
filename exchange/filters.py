import django_filters

from exchange.models import ProductList


class ProductListFilter(django_filters.FilterSet):
    star = django_filters.NumberFilter(field_name="product__star", lookup_expr="gte")

    class Meta:
        model = ProductList
        fields = ('category', 'type', 'stage_level', 'name')
