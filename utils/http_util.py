import copy
import json
import os
from pathlib import Path
from typing import List, Dict

from Maple.settings.base import MEDIA_ROOT, STATIC_ROOT
from exchange.models import product_list_image_path, ProductList
from storages.google import BUCKET

from django.http import HttpResponse


def extract_dataset_by_folder(from_folder: str) -> List[Dict[str, str]]:
    from_directory = Path(STATIC_ROOT, from_folder)
    from_directory = list(os.walk(from_directory))
    data_path_len = len(Path(from_directory[0][0]).parts)
    from_directory_folder = from_directory[1:]
    folder_structure_of_data = ["category", "type", "career", "stage_name"]
    
    dataset = list()
    for i, folder in enumerate(from_directory_folder):
        folder_path_names = Path(folder[0]).parts[data_path_len::]
        if folder[1]:
            continue
        
        data = dict()
        for j, name in enumerate(folder_path_names):
            if j == 2 and name.startswith(ProductList.Career.Null):
                continue
            data[folder_structure_of_data[j]] = name
        
        for k, image in enumerate(folder[2]):
            _data = copy.copy(data)
            image_name = image.split(".jpg")[0]
            image = product_list_image_path("", image)
            image_path = Path(folder[0], folder[2][k])
            _data["name"] = image_name
            _data["image"] = image
            _data["image_path"] = image_path
            dataset.append(_data)
    return dataset


def upload_file_to_gcp_storage(blob_name: str, filename_path: str) -> None:
    """
    上傳檔案到gcp storage
    :param blob_name: "product_image/10a31dfe47.PNG"
    :param filename_path: "static\default_images\武器\弓\烏特卡勒德之弓.jpg"
    :return:
    """
    blob = BUCKET.blob(blob_name)
    blob.upload_from_filename(filename_path)


def is_file_exist(blob_name: str):
    return BUCKET.blob(blob_name).exists()


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


def jsonify_unauthorized(*args, **kwargs):
    content = json.dumps(
        dict(*args, **kwargs),
        ensure_ascii=False
    )
    return HttpResponseUnauthorized(
        content,
        content_type='application/json'
    )


def jsonify(data_status=0, data_msg='ok', results=None,
            http_status=None, **kwargs):
    encoded_data = json.dumps(dict(
        data_status=data_status,
        data_msg=data_msg,
        results=results,
        http_status=http_status,
        **kwargs),
        ensure_ascii=False,
    )
    
    return HttpResponse(
        encoded_data,
        content_type="application/json"
    )
