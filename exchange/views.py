from typing import Optional

from data_spec_validator.decorator import dsv
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from exchange.models import ProductList, Product
from exchange.serializer import ProductListSerializer, ProductSerializer
from utils.convert_util import ProductConverter
from utils.params_spec_util import ProductListSpec, extract_request_param_data, ProductSpec


class ProductListViewSet(viewsets.ModelViewSet):
    queryset = ProductList.objects.all()
    serializer_class = ProductListSerializer
    
    def list(self, request, *args, **kwargs):
        # todo: eval特定的欄位格式
        product_list_data = filter_params_to_query_product_list(self.request, self.get_serializer_class())
        product_list_data = self.filter_product_by_params(product_list_data)
        return Response(product_list_data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data = self.filter_product_by_params([data])
        return Response(data)
    
    def filter_product_by_params(self, product_list_data):
        for data in product_list_data:
            product = filter_params_to_query_product(self.request, data["product_list_id"])
            data["count"] = product.count()
            min_price = max_price = 0
            if product:
                min_price = product.first().price
                max_price = product.last().price
            data["min_price"] = min_price
            data["max_price"] = max_price
        return product_list_data
    
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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def list(self, request, *args, **kwargs):
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        
        self.queryset = Product.objects.filter(
            product_list__pk=request.query_params["id"], create_date__gte=two_days_ago
        )
        return super(ProductViewSet, self).list(request, *args, **kwargs)
    
    # def get_queryset(self):
    #     qs = Product.objects.all()
    #     qs = self.serializer_class.setup_eager_loading(qs)
    #     return qs


#########################
# 以下放判斷params的func #
#########################

@dsv(ProductListSpec)
def filter_params_to_query_product_list(request, serializer_class):
    param_data = extract_request_param_data(ProductListSpec, request.query_params.dict())
    queryset = ProductList.objects.filter(**param_data)
    serializer = serializer_class(queryset, many=True)
    return serializer.data


@dsv(ProductSpec)
def filter_params_to_query_product(request, product_list_id: Optional[int] = None, serializer_class=None):
    param_data = extract_request_param_data(ProductSpec, request.query_params.dict(), ProductConverter)
    
    if serializer_class:
        queryset = Product.objects.filter(**param_data)
        serializer = serializer_class(queryset, many=True)
        return serializer.data
    else:
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        queryset = Product.objects.filter(
            product_list__product_list_id=product_list_id,
            create_date__gte=two_days_ago, **param_data
        )
        return queryset

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
