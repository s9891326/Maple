import django_filters

from accounts.models import CustomUser
from coins.models import Coin


class CoinFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    value = django_filters.NumberFilter(field_name="value", lookup_expr="gte")
    total = django_filters.NumberFilter(field_name="total", lookup_expr="gte")
    server_name = django_filters.ChoiceFilter(
        field_name="server_name", choices=CustomUser.ServerName.get_valid_server_name())
    
    class Meta:
        model = Coin
        fields = ("title", "value", "total", "server_name",)
