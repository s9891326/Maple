from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from exchange.models import EquipLibrary, Equip
from exchange.serializer import EquipLibrarySerializer, EquipSerializer


class EquipLibraryViewSet(viewsets.ModelViewSet):
    queryset = EquipLibrary.objects.all()
    serializer_class = EquipLibrarySerializer


# class EquipView(viewsets.ModelViewSet):
#     queryset = Equip.objects.all()
#     serializer_class = EquipSerializer


class EquipView(APIView):
    def get(self, request):
        all_images = Equip.objects.all()
        serializer = EquipSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request):
        file_serializer = EquipSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
