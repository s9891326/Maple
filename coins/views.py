from rest_framework import viewsets

from coins.models import Coin
from coins.serializer import CoinSerializer


class CoinViewSet(viewsets.ModelViewSet):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
