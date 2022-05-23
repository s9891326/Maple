import logging
import random

from pathlib import Path
from django.db import connection
from django.http import JsonResponse

from Maple.settings import base
from exchange.models import ProductList, Product, product_list_image_path
from exchange.serializer import ProductSerializer, ProductListSerializer
from utils.util import extract_dataset_by_folder, upload_file_to_gcp_storage


def add_product_list(request):
    from_folder = "default_images"
    to_folder = "product_list_image_default"
    dataset = extract_dataset_by_folder(from_folder, to_folder, default_image_path=product_list_image_path)
    
    # 移除共用、死靈兩種階級
    product_list_stage = ProductList.Stage.values
    product_list_stage.remove(ProductList.Stage.Share.value)
    product_list_stage.remove(ProductList.Stage.DeadBlue.value)
    product_list_data = list()
    for category, data_list in dataset.items():
        for data in data_list:
            for product_list_type, name_and_image in data.items():
                for name, image in name_and_image.items():
                    for stage_level in product_list_stage:
                        product_list_data.append(dict(
                            category=category,
                            type=product_list_type,
                            name=name,
                            stage_level=stage_level,
                            image=image
                        ))
    
    product_list_obj = [ProductList(**data) for data in product_list_data]
    ProductList.objects.bulk_create(product_list_obj)
    
    blob_names = set()
    for obj in product_list_obj:
        blob_name = str(obj.image).replace("\\", "/")
        if blob_name not in blob_names:
            upload_file_to_gcp_storage(
                blob_name, Path(base.STATIC_ROOT, from_folder, obj.category, obj.type, f"{obj.name}.jpg")
            )
            blob_names.add(blob_name)
    
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
            price=random.randint(100000, 300000)
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


def test(request):
    logging.warning("eddy test")
    return JsonResponse({"success": True}, safe=False)
