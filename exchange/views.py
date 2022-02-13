from data_spec_validator.decorator import dsv
from django.db.models import QuerySet
from django.shortcuts import render
from django.utils import timezone
from django_filters import rest_framework

from rest_framework import viewsets, status
from rest_framework.decorators import action

from exchange.filters import ProductListFilter, ProductFilter
from exchange.forms import ProductListForm
from exchange.models import ProductList, Product
from exchange.serializer import ProductListSerializer, ProductSerializer
from utils.convert_util import ProductConverter
from utils.params_spec_util import ProductListSpec, extract_request_param_data, ProductSpec
from utils.response import APIResponse
from utils.status_message import StatusMessage


class ProductListViewSet(viewsets.ModelViewSet):
    queryset = ProductList.objects.all()
    serializer_class = ProductListSerializer
    
    # fixme: 或許可以改用django-filter來改寫底下的list()
    # filter_backends = (rest_framework.DjangoFilterBackend,)
    # filter_class = ProductListFilter
    
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        result = valid_form_update_query_params(request, ProductListForm)
        if isinstance(result, APIResponse):
            return result
        request = result
        
        product_list_queryset = filter_params_to_query_product_list(request)
        serializer = self.get_serializer(product_list_queryset, many=True)
        result = filter_params_to_query_product(request, serializer.data)
        return APIResponse(
            data_status=status.HTTP_200_OK,
            data_msg=StatusMessage.HTTP_200_OK.value,
            results=result,
            status=status.HTTP_200_OK,
        )
    
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
    
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filter_class = ProductFilter


#########################
# 以下放判斷params的func #
#########################

@dsv(ProductListSpec)
def filter_params_to_query_product_list(request) -> QuerySet:
    param_data = extract_request_param_data(ProductListSpec, request.query_params.dict())
    queryset = ProductList.objects.filter(**param_data)
    return queryset


@dsv(ProductSpec)
def filter_params_to_query_product(request, product_list_data):
    param_data = extract_request_param_data(ProductSpec, request.query_params.dict(), ProductConverter)
    
    for data in product_list_data:
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        product = Product.objects.filter(
            product_list__product_list_id=data["product_list_id"],
            create_date__gte=two_days_ago, **param_data
        )
        data["count"] = product.count()
        min_price = max_price = 0
        if product:
            min_price = product.first().price
            max_price = product.last().price
        data["min_price"] = min_price
        data["max_price"] = max_price
    
    return product_list_data


def valid_form_update_query_params(request, form):
    form = form(request.query_params)
    if form.is_valid():
        request.query_params._mutable = True
        clean_data = {k: v for k, v in form.clean().items() if v != "" and v is not None and k in form.data.keys()}
        request.query_params.clear()
        request.query_params.update(clean_data)
        return request
    else:
        return APIResponse(
            data_status=status.HTTP_400_BAD_REQUEST,
            data_msg=StatusMessage.HTTP_400_BAD_FORM_VALID.value,
            status=status.HTTP_400_BAD_REQUEST,
        )

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
