from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from exchange.models import EquipLibrary, Equip
from exchange.serializer import EquipLibrarySerializer, EquipSerializer


class EquipLibraryViewSet(viewsets.ModelViewSet):
    queryset = EquipLibrary.objects.all()
    serializer_class = EquipLibrarySerializer


class EquipViewSet(viewsets.ModelViewSet):
    # queryset = Equip.objects.all()
    serializer_class = EquipSerializer

    def get_queryset(self):
        # todo: 排成刷新武器庫最大最小的價格 因為武器有不同的上架時間
        # 上架道具限時48小時，時間到不顯示
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        return Equip.objects.filter(create_date__gte=two_days_ago).order_by("price")

# class EquipView(APIView):
#     def get(self, request):
#         all_images = Equip.objects.all()
#         serializer = EquipSerializer(all_images, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     def post(self, request):
#         file_serializer = EquipSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_serializer.save()
#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
