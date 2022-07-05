import django_filters

from coins.models import Coin


class CoinFilter(django_filters.FilterSet):
    total = django_filters.NumberFilter(field_name="total", lookup_expr="gte")
    
    class Meta:
        model = Coin
        fields = ("total",)
