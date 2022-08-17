from django_filters import rest_framework
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from coins.filters import CoinFilter
from coins.models import Coin
from coins.serializer import CoinSerializer
from utils import error_msg
from utils.util import CustomModelViewSet


class CoinViewSet(CustomModelViewSet):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    
    filter_class = CoinFilter
    ordering_fields = ("update_date",)
    ordering = ("update_date",)
    
    def partial_update(self, request, *args, **kwargs):
        create_by = request.user
        instance = self.get_object()
        
        if create_by != instance.create_by:
            return Response(error_msg.CREATE_BY_NOT_CORRECT, status=status.HTTP_400_BAD_REQUEST)
        
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=False, url_path="sell-coin")
    def get_sell_coin(self, request):
        """
        取得該使用者上架的賣幣列表
        :param request:
        :return:
        """
        create_by = request.user
        queryset = Coin.objects.filter(create_by=create_by)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
