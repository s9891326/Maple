import os
import shutil
from pathlib import Path

from django.db import connection
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from rest_framework import status

from Maple.settings import STATIC_ROOT, MEDIA_ROOT
from exchange.models import ProductList, Product
from exchange.serializer import ProductSerializer, ProductListSerializer


def add(request):
    product_list_image_default_folder = "product_list_image_default"
    from_directory = Path(STATIC_ROOT, "images", "product_list")
    to_directory = Path(MEDIA_ROOT, product_list_image_default_folder)
    
    if not os.path.exists(to_directory):
        os.makedirs(to_directory)
    
    from_directory = list(os.walk(from_directory))
    data_type = from_directory[0][1]
    from_directory_folder = from_directory[1:]
    
    # {
    #     "雙手劍": {
    #         "傑伊西恩雙手劍": "product_list_image_default/0_0.jpg"
    #     }
    # }
    dataset = dict()
    
    for i, folder in enumerate(from_directory_folder):
        folder_name = folder[0]
        data = dict()
        for k, image in enumerate(folder[2]):
            image_name = image.split(".")[0]
            image_rename = f"{i}_{k}.jpg"
            image_path = f"product_list_image_default/{image_rename}"
            shutil.copyfile(Path(folder_name, image), Path(to_directory, image_rename))
            data[image_name] = image_path
        dataset[data_type[i]] = data

    product_list_data = list()
    for product_list_type, product_list_name_and_image in dataset.items():
        for name, image in product_list_name_and_image.items():
            for stage_level in ProductList.Stage:
                product_list_data.append(dict(
                    category=ProductList.Category.Weapon.value,
                    type=product_list_type,
                    name=name,
                    stage_level=stage_level.value,
                    image=image
                ))
    # product_list_data = [
    #     dict(
    #         category=ProductList.Category.Weapon.value,
    #         type="雙手劍",
    #         name="普錫杰勒雙手劍",
    #         stage_level=ProductList.Stage.White.value
    #     ),
    #     dict(
    #         category=ProductList.Category.Weapon.value,
    #         type="雙手劍",
    #         name="傑伊西恩雙手劍",
    #         stage_level=ProductList.Stage.White.value
    #     ),
    #     dict(
    #         category=ProductList.Category.Weapon.value,
    #         type="長槍",
    #         name="普錫杰勒之槍",
    #         stage_level=ProductList.Stage.White.value
    #     ),
    #     dict(
    #         category=ProductList.Category.Weapon.value,
    #         type="長槍",
    #         name="傑伊希恩之槍",
    #         stage_level=ProductList.Stage.White.value
    #     ),
    #     dict(
    #         category=ProductList.Category.Armor.value,
    #         type="帽子",
    #         name="伊克雷帝帽",
    #         stage_level=ProductList.Stage.White.value
    #     ),
    #     dict(
    #         category=ProductList.Category.Armor.value,
    #         type="帽子",
    #         name="伊克雷帝海王星帽",
    #         stage_level=ProductList.Stage.White.value
    #     ),
    #     dict(
    #         category=ProductList.Category.Armor.value,
    #         type="套服",
    #         name="伊克雷帝勇士鎧甲",
    #         stage_level=ProductList.Stage.White.value
    #     ),
    #     dict(
    #         category=ProductList.Category.Armor.value,
    #         type="套服",
    #         name="伊克雷帝奧丁神袍",
    #         stage_level=ProductList.Stage.White.value
    #     ),
    #     dict(
    #         category=ProductList.Category.Skins.value,
    #         type="武器",
    #         name="不漂釀捏",
    #     ),
    #     dict(
    #         category=ProductList.Category.Skins.value,
    #         type="武器",
    #         name="培根武器",
    #     ),
    #     dict(
    #         category=ProductList.Category.Consumables.value,
    #         type="椅子",
    #         name="充滿願望的紙飛機",
    #     ),
    #     dict(
    #         category=ProductList.Category.Consumables.value,
    #         type="椅子",
    #         name="冰淇淋女王卡車",
    #     )
    # ]

    product_list_obj = [ProductList(**data) for data in product_list_data]
    ProductList.objects.bulk_create(product_list_obj)

    # product_data = [
    #     dict(
    #         product_list=ProductList.objects.get(name="普錫杰勒之槍"),
    #         star=0,
    #         level=1,
    #         total_level=15,
    #         is_maple=False,
    #         maple_capability=Product.Maple.none,
    #         maple_level=0,
    #         price=181986
    #     ),
    #     dict(
    #         product_list=ProductList.objects.get(name="普錫杰勒之槍"),
    #         star=0,
    #         level=1,
    #         total_level=15,
    #         is_maple=False,
    #         maple_capability=Product.Maple.none,
    #         maple_level=0,
    #         price=182088
    #     ),
    #     dict(
    #         product_list=ProductList.objects.get(name="傑伊西恩雙手劍"),
    #         star=0,
    #         level=1,
    #         total_level=10,
    #         is_maple=False,
    #         maple_capability=Product.Maple.none,
    #         maple_level=0,
    #         price=199899
    #     ),
    #     dict(
    #         product_list=ProductList.objects.get(name="普錫杰勒雙手劍"),
    #         star=0,
    #         level=1,
    #         total_level=10,
    #         is_maple=False,
    #         maple_capability=Product.Maple.none,
    #         maple_level=0,
    #         price=222046
    #     ),
    #     dict(
    #         product_list=ProductList.objects.get(name="傑伊希恩之槍"),
    #         star=0,
    #         level=1,
    #         total_level=15,
    #         is_maple=False,
    #         maple_capability=Product.Maple.none,
    #         maple_level=0,
    #         price=442630
    #     ),
    #     dict(
    #         product_list=ProductList.objects.get(name="傑伊希恩之槍"),
    #         star=0,
    #         level=1,
    #         total_level=15,
    #         is_maple=False,
    #         maple_capability=Product.Maple.none,
    #         maple_level=0,
    #         price=442971
    #     )
    # ]
    # product_obj = [Product(**data) for data in product_data]
    # Product.objects.bulk_create(product_obj)
    
    results = []
    dataset = ProductList.objects.all().prefetch_related('product')
    for data in dataset:
        # result = model_to_dict(data)
        # result["image"] = result["image"].name
        # result = ProductListSerializer(data).data
        # result["product"] = ProductSerializer(data.product.all(), many=True).data
        results.append(ProductListSerializer(data).data)
    return JsonResponse(results, safe=False)


def delete(request):
    ProductList.objects.all().delete()
    data = list(ProductList.objects.all().values())
    return JsonResponse(data, safe=False)


def drop_table(request):
    cursor = connection.cursor()
    cursor.execute('''Drop table IF Exists exchange_productimage''')
    cursor.execute('''Drop table IF Exists exchange_product''')
    cursor.execute('''Drop table IF Exists exchange_productlist''')
    cursor.execute('''DELETE FROM django_migrations WHERE app = "exchange"''')
    return JsonResponse({"data": "drop all exchange table."}, safe=False)
