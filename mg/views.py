import copy
import logging
import random

from pathlib import Path
from django.db import connection
from django.http import JsonResponse

from Maple.settings import base
from accounts.models import CustomUser
from exchange.models import ProductList, Product
from exchange.serializer import ProductSerializer, ProductListSerializer
from utils.util import extract_dataset_by_folder, upload_file_to_gcp_storage, is_file_exist

FROM_FOLDER = "default_images"


def add_product_list(request):
    dataset = extract_dataset_by_folder(FROM_FOLDER)
    
    # 移除共用、死靈兩種階級
    product_list_stage = ProductList.Stage.values
    product_list_stage.remove(ProductList.Stage.Share.value)
    product_list_stage.remove(ProductList.Stage.DeadBlue.value)
    product_list_data = list()
    product_list_images_path = list()
    
    for data in dataset:
        for stage_level in product_list_stage:
            _data = copy.copy(data)
            _data["stage_level"] = _data.get("stage_level", stage_level)
            product_list_images_path.append(_data.pop("image_path"))
            product_list_data.append(_data)
            if data.get("stage_level") == ProductList.Stage.Share.value:
                break
    
    product_list_obj = [ProductList(**data) for data in product_list_data]
    ProductList.objects.bulk_create(product_list_obj)
    
    results = []
    dataset = ProductList.objects.all()[:10].prefetch_related('product')
    for data in dataset:
        # result = model_to_dict(data)
        # result["image"] = result["image"].name
        # result = ProductListSerializer(data).data
        # result["product"] = ProductSerializer(data.product.all(), many=True).data
        results.append(ProductListSerializer(data).data)
    return JsonResponse(results, safe=False)


def delete_product_list(request):
    ProductList.objects.all().delete()
    data = list(ProductList.objects.all().values())
    return JsonResponse(data, safe=False)


def add_product(request):
    product_data = list()
    map_capability_choice = Product.MapleCapability.values
    map_capability_choice.remove(Product.MapleCapability.Null)
    
    # 伺服器
    server_name_choice = CustomUser.ServerName.get_valid_server_name()
    server_name_choice = [server_name[0] for server_name in server_name_choice]
    
    if base.DJANGO_SETTINGS_MODULE == base.LOCAL_MODE:
        create_by = CustomUser.objects.get(username="root")
    else:
        create_by = CustomUser.objects.get(username="admin")
    
    for product_list_id in ProductList.objects.all().values_list("product_list_id", flat=True).iterator():
        # 楓底
        is_maple = random.choice([True, False])
        maple_capability = Product.MapleCapability.Null
        maple_level = 0
        if is_maple:
            maple_capability = random.choice(map_capability_choice)
            maple_level = random.randint(0, 10)
        
        # 淺力
        potential_level = random.choice(Product.Potential.values)
        potential_capability = "最大MP:330,命中力8"
        if potential_level == Product.Potential.Null:
            potential_capability = ""
        
        # 星火
        spark_level = random.choice(Product.Spark.values)
        spark_capability = "經驗值比例轉魔攻,經驗值比例轉物攻"
        if spark_level == Product.Spark.Null:
            spark_capability = ""
        
        # 靈魂
        is_equippable_soul = random.choice([True, False])
        soul_capability = None
        if is_equippable_soul:
            soul_capability = "test_soul"
        
        product_data.append(dict(
            product_list=ProductList.objects.get(product_list_id=product_list_id),
            star=random.randint(0, 30),
            level=random.choice([1, 5, 10]),
            total_level=random.choice([15, 30, 35]),
            cut_num=random.randint(0, 10),
            attack=random.randint(100, 200),
            potential_level=potential_level,
            potential_capability=potential_capability,
            spark_level=spark_level,
            spark_capability=spark_capability,
            is_equippable_soul=is_equippable_soul,
            soul_capability=soul_capability,
            is_maple=is_maple,
            maple_capability=maple_capability,
            maple_level=maple_level,
            price=random.randint(100000, 300000),
            title="商品標題",
            server_name=random.choice(server_name_choice),
            create_by=create_by
        ))
    
    product_obj = [Product(**data) for data in product_data]
    Product.objects.bulk_create(product_obj)
    
    queryset = Product.objects.all()[:10]
    serializer = ProductSerializer(queryset, many=True)
    
    return JsonResponse(serializer.data, safe=False)


def delete_product(request):
    Product.objects.all().delete()
    data = list(Product.objects.all().values())
    return JsonResponse(data, safe=False)


def drop_table(request):
    cursor = connection.cursor()
    cursor.execute('''Drop table IF Exists exchange_productimage''')
    cursor.execute('''Drop table IF Exists exchange_product''')
    cursor.execute('''Drop table IF Exists exchange_productlist''')
    cursor.execute('''DELETE FROM django_migrations WHERE app = "exchange"''')
    return JsonResponse({"data": "drop all exchange table."}, safe=False)


def upload_image_to_gcp_storage(request):
    dataset = extract_dataset_by_folder(FROM_FOLDER)
    product_list_image = ProductList.objects.values_list("image", flat=True).distinct()
    if base.DJANGO_SETTINGS_MODULE == base.HEROKU_MODE:
        assert len(dataset) == len(product_list_image), "Error dataset and product_list different amount."
        blob_names = set()
        for i, obj in enumerate(product_list_image):
            blob_name = str(obj).replace("\\", "/")
            if blob_name not in blob_names and not is_file_exist(blob_name):
                upload_file_to_gcp_storage(blob_name, dataset[i]["image_path"])
                blob_names.add(blob_name)
    return JsonResponse("success", safe=False)


def test(request):
    logging.warning("eddy test")
    return JsonResponse("success", safe=False)

# import requests
# data = dict(
#     grant_type='authorization_code',
#     code=str(request.GET['code']),
#     redirect_uri='http://localhost:8000/mg/test',
#     client_id='1657301302',
#     client_secret='f3dd69c65da480f04d18bdf504499016'
# )
# headers = {'Content-type': 'application/x-www-form-urlencoded'}
# rsp = requests.post('https://api.line.me/oauth2/v2.1/token', data, headers=headers)
# return JsonResponse(rsp.text, safe=False)

# {
#   "access_token": "eyJhbGciOiJIUzI1NiJ9.4fSsz3wrgqZEsHQxZ8ay4D4qqom2IrcKIXIoDj-aN_Dughfl3JjFTZLDggdqjp4a6LNNXOgHnZXY1apXLBwEz23QDGB39KZjqsZ-_zag_qZxrIVeEW6LyM5dFfOYxSj2sfr7vnSi7Vg7hEooXcmrSEbdKVGYAXtMwal4ze5HrMI.nLYGtH4nyI6RG_R55SMff50iGmcL1MNcgFX9JMkflBI",
#   "token_type": "Bearer",
#   "refresh_token": "c48hfkT4xMSI5q2VTTEy",
#   "expires_in": 2592000,
#   "scope": "profile openid",
#   "id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FjY2Vzcy5saW5lLm1lIiwic3ViIjoiVTYyYjc5ODM2NDNhNDI4M2QzNTRmZWE0MWU4YTUxYmM5IiwiYXVkIjoiMTY1NzMwMTMwMiIsImV4cCI6MTY1ODA2ODM0NCwiaWF0IjoxNjU4MDY0NzQ0LCJub25jZSI6IjIwMjIwNzE3IiwiYW1yIjpbInB3ZCJdLCJuYW1lIjoi546L5b2l5reHIiwicGljdHVyZSI6Imh0dHBzOi8vcHJvZmlsZS5saW5lLXNjZG4ubmV0LzBoX3Y5YzliODhBRmtFR2hhdkhfVl9EamhmRGpSek5BWVJmSGxPYWlFWVhXNTVJazRQT1g5SFBpUWFXRHdvSWhjR1B5c2JQU1FTV1RrciJ9.DKARBlc7Qki_3tkM90T0zT_gJ2Cxz1tct5RzIeNn6xE"
# }


# curl -v -X POST 'https://api.line.me/oauth2/v2.1/verify' \
#  -d 'id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FjY2Vzcy5saW5lLm1lIiwic3ViIjoiVTYyYjc5ODM2NDNhNDI4M2QzNTRmZWE0MWU4YTUxYmM5IiwiYXVkIjoiMTY1NzMwMTMwMiIsImV4cCI6MTY1ODA2ODM0NCwiaWF0IjoxNjU4MDY0NzQ0LCJub25jZSI6IjIwMjIwNzE3IiwiYW1yIjpbInB3ZCJdLCJuYW1lIjoi546L5b2l5reHIiwicGljdHVyZSI6Imh0dHBzOi8vcHJvZmlsZS5saW5lLXNjZG4ubmV0LzBoX3Y5YzliODhBRmtFR2hhdkhfVl9EamhmRGpSek5BWVJmSGxPYWlFWVhXNTVJazRQT1g5SFBpUWFXRHdvSWhjR1B5c2JQU1FTV1RrciJ9.DKARBlc7Qki_3tkM90T0zT_gJ2Cxz1tct5RzIeNn6xE' \
#  -d 'client_id=1657301302'

# curl -v -X POST https://api.line.me/oauth2/v2.1/token \
# -H 'Content-Type: application/x-www-form-urlencoded' \
# -d 'grant_type=authorization_code' \
# -d 'code='uUXDNXOvxlTlOb8YRxR9'' \
# --data-urlencode 'redirect_uri=http://localhost:8000/mg/test' \
# -d 'client_id=1657301302' \
# -d 'client_secret=f3dd69c65da480f04d18bdf504499016'
