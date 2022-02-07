from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from exchange.models import EquipLibrary, Equip
from exchange.serializer import EquipLibrarySerializer, EquipSerializer


class EquipLibraryViewSet(viewsets.ModelViewSet):
    queryset = EquipLibrary.objects.all()
    serializer_class = EquipLibrarySerializer
    
    # @action(detail=True)
    # def equip(self, request, pk):
    #     """
    #     http://127.0.0.1:8000/v1/exchange/api/equip-library/2/equip
    #     在原本的api url path後面增加對應的接口
    #     :param request:
    #     :param pk:
    #     :return:
    #     """
    #     # 上架道具限時48小時，時間到不顯示
    #     two_days_ago = timezone.now() - timezone.timedelta(days=2)
    #     data = Equip.objects.filter(
    #         equip_library__pk=pk, create_date__gte=two_days_ago
    #     ).prefetch_related("equip_image").values()
    #     serializer = EquipSerializer(data, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class EquipViewSet(viewsets.ModelViewSet):
    queryset = Equip.objects.all()
    serializer_class = EquipSerializer

    def list(self, request, *args, **kwargs):
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        
        if request.data and request.data.get("id", 0):
            self.queryset = Equip.objects.filter(
                equip_library__pk=request.data["id"], create_date__gte=two_days_ago
            )
        return super(EquipViewSet, self).list(request, *args, **kwargs)

    # def get_queryset(self):
    #     qs = Equip.objects.all()
    #     qs = self.serializer_class.setup_eager_loading(qs)
    #     return qs

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
