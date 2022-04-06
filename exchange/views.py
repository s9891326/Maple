from distutils.util import strtobool

from data_spec_validator.decorator import dsv
from django.db.models import QuerySet
from django.utils import timezone
from django_filters import rest_framework

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from exchange.filters import ProductListFilter, ProductFilter
from exchange.forms import ProductListForm
from exchange.models import ProductList, Product
from exchange.serializer import ProductListSerializer, ProductSerializer
from utils.convert_util import ProductConverter, ProductListConverter
from utils.params_spec_util import ProductListSpec, extract_request_param_data, ProductSpec
from utils.response import common_finalize_response


class ProductListViewSet(viewsets.ModelViewSet):
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
    
    def finalize_response(self, request, response, *args, **kwargs):
        return common_finalize_response(super().finalize_response, request, response, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    ordering_fields = ["star", "price"]
    ordering = ["price"]
    
    def finalize_response(self, request, response, *args, **kwargs):
        return common_finalize_response(super().finalize_response, request, response, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        self.filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
        self.filter_class = ProductFilter
        return super().list(request, *args, **kwargs)


#########################
# 以下放判斷params的func #
#########################

@dsv(ProductListSpec)
def extract_params_to_query_product_list(request) -> QuerySet:
    param_data = extract_request_param_data(ProductListSpec, request.query_params.dict(), ProductListConverter)
    queryset = ProductList.objects.filter(**param_data)
    return queryset


@dsv(ProductSpec)
def extract_params_to_query_product(request, product_list_data):
    param_data = extract_request_param_data(ProductSpec, request.query_params.dict(), ProductConverter)
    two_days_ago = timezone.now() - timezone.timedelta(days=2)
    
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


def update_query_params(request, form):
    form = form(request.query_params)
    if form.is_valid():
        request.query_params._mutable = True
        clean_data = {k: v for k, v in form.clean().items() if v != "" and v is not None and k in form.data.keys()}
        request.query_params.clear()
        request.query_params.update(clean_data)
    else:
        return form.errors

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
