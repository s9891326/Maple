from distutils.util import strtobool
from typing import Dict, Any

from data_spec_validator.decorator import dsv
from django.db.models import QuerySet
from django_filters import rest_framework

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import CustomUser
from exchange.filters import ProductFilter
from exchange.forms import ProductListForm
from exchange.models import ProductList, Product
from exchange.serializer import ProductListSerializer, ProductSerializer
from utils import error_msg
from utils.convert_util import ProductConverter, ProductListConverter
from utils.params_spec_util import ProductListSpec, extract_request_param_data, ProductSpec
from utils.util import get_two_days_ago, CustomModelViewSet, update_query_params


class ProductListViewSet(CustomModelViewSet):
    queryset = ProductList.objects.all()
    serializer_class = ProductListSerializer
    
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name", "stage_level"]
    ordering = ["stage_level", "name"]
    
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
        error = update_query_params(request, ProductListForm)
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
        product_list_queryset = extract_params_to_query_product_list(request)
        product_list_queryset = self.filter_queryset(product_list_queryset)
        serializer = self.get_serializer(product_list_queryset, many=True)
        result = extract_params_to_query_product(request, serializer.data)
        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, url_path="product-column")
    def get_product_column(self, request):
        """
        獲取所有商品列類別-種類-裝備名稱
        "武器": {
            "古代之弓": [
                "以弗索古代之弓",
                "傑伊希恩古代之弓",
                "普錫杰勒古代之弓",
                "烏特卡勒德古代之弓"
            ],...
        }
        :param request:
        :return:
        """
        # 是否要顯示商品名稱
        has_display_name = strtobool(request.query_params.get("has_display_name", '0'))
        product_columns = ProductList.objects.values(
            "category", "type", "name"
        ).order_by("category", "type", "name").distinct()
        results = {}
        
        if has_display_name:
            for product_column in product_columns:
                product_type_of_name = results.get(product_column["category"], {})
                name = product_type_of_name.get(product_column["type"], set())
                name.add(product_column["name"])
                product_type_of_name[product_column["type"]] = name
                results[product_column["category"]] = product_type_of_name
        else:
            for product_column in product_columns:
                category = results.get(product_column["category"], set())
                category.add(product_column["type"])
                results[product_column["category"]] = category
        
        return Response(results, status=status.HTTP_200_OK)


class ProductViewSet(CustomModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    ordering_fields = ["star", "price"]
    ordering = ["server_name", "price"]
    
    def list(self, request, *args, **kwargs):
        # query_params = request.query_params
        # user = request.user
        # 如果使用者沒有篩選商品的伺服器，則去用戶資料看用戶是否有設定預設伺服器
        # if not query_params.get("server_name") and user.server_name != CustomUser.ServerName.Null:
        #     request.query_params._mutable = True
        #     request.query_params['server_name'] = user.server_name
        self.filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
        self.filter_class = ProductFilter
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        override destroy function.
        增加判斷當前token內的使用者 跟 刪除的商品使用者是否一樣
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        if self.request.user != instance.create_by:
            return Response(error_msg.CREATE_BY_NOT_CORRECT, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, url_path="sell-product")
    def get_sell_product(self, request):
        """
        取得該使用者上架的商品，排除已經下架的商品
        :param request:
        :return:
        """
        ordering_filed = request.query_params.get('ordering', '-update_date')
        create_by = request.user
        queryset = Product.objects.filter(
            update_date__gte=get_two_days_ago(), create_by=create_by
        ).order_by(ordering_filed)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#########################
# 以下放判斷params的func #
#########################

@dsv(ProductListSpec)
def extract_params_to_query_product_list(request) -> QuerySet:
    """
    針對輸入進來的參數進行product_list表的查詢，並針對特定欄位進行格式判斷
    :param request:
    :return:
    """
    param_data = extract_request_param_data(ProductListSpec, request.query_params.dict(), ProductListConverter)
    
    # 如果有指定職業進行搜尋，則主動帶入'共用'職業進行搜尋
    career_data = param_data.get('career__in', [])
    if career_data:
        career_data.append(ProductList.Career.Share.value)
    
    queryset = ProductList.objects.filter(**param_data)
    return queryset


@dsv(ProductSpec)
def extract_params_to_query_product(request, product_list_data) -> Dict[str, Any]:
    """
    針對輸入進來的參數進行product表的查詢，並針對特定欄位進行格式判斷
    :param request:
    :return:
    """
    param_data = extract_request_param_data(ProductSpec, request.query_params.dict(), ProductConverter)
    two_days_ago = get_two_days_ago()
    
    for data in product_list_data:
        product = Product.objects.filter(
            product_list__product_list_id=data["product_list_id"],
            update_date__gte=two_days_ago, **param_data
        )
        data["count"] = product.count()
        min_price = max_price = 0
        if product:
            min_price = product.order_by("price").first().price
            max_price = product.order_by("price").last().price
        data["min_price"] = min_price
        data["max_price"] = max_price
    
    return product_list_data

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
