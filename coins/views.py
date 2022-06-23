from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from coins.models import Coin
from coins.serializer import CoinSerializer
from utils import error_msg
from utils.util import CustomModelViewSet


class CoinViewSet(CustomModelViewSet):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        # 確保聯絡方式 = 'other'時，需要有contact_explanation欄位的值
        if data["contact_method"] == Coin.ContactMethod.Other.value and not data.get("contact_explanation"):
            return Response(error_msg.MUST_HAVE_THIS_COLUMN % "contact_explanation", status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        create_by = request.user
        instance = self.get_object()
        data = request.data
        
        if create_by != instance.create_by:
            return Response(error_msg.CREATE_BY_NOT_CORRECT, status=status.HTTP_400_BAD_REQUEST)
        
        # 確保聯絡方式 = 'other'時，需要有contact_explanation欄位的值
        if data.get("contact_method") == Coin.ContactMethod.Other.value and not data.get("contact_explanation"):
            return Response(error_msg.MUST_HAVE_THIS_COLUMN % "contact_explanation", status=status.HTTP_400_BAD_REQUEST)
        
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
