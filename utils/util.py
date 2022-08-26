import copy
import json
import os
import shutil
from pathlib import Path
from typing import List, Dict

from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from Maple.settings.base import MEDIA_ROOT, STATIC_ROOT
from exchange.models import product_list_image_path, ProductList
from storages.google import BUCKET
from utils import error_msg

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def extract_dataset_by_folder(from_folder: str) -> List[Dict[str, str]]:
    from_directory = Path(STATIC_ROOT, from_folder)
    from_directory = list(os.walk(from_directory))
    data_path_len = len(from_directory[0][0].split("\\"))
    from_directory_folder = from_directory[1:]
    folder_structure_of_data = ["category", "type", "career"]
    
    dataset = list()
    for i, folder in enumerate(from_directory_folder):
        folder_path_names = folder[0].split("\\")[data_path_len::]
        if folder[1]:
            continue
        
        data = dict()
        for j, name in enumerate(folder_path_names):
            if j == 2 and name.startswith(ProductList.Career.Null):
                data["stage_level"] = ProductList.Stage.Share.value
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


def upload_file_to_gcp_storage(blob_name: str, filename_path: str):
    """
    上傳檔案到gcp storage
    :param blob_name: "product_image/10a31dfe47.PNG"
    :param filename_path: "static\default_images\武器\弓\烏特卡勒德之弓.jpg"
    :return:
    """
    blob = BUCKET.blob(blob_name)
    blob.upload_from_filename(filename_path)


def get_two_days_ago():
    return timezone.localtime(timezone.now() - timezone.timedelta(days=2))


def common_finalize_response(finalize_response, request, response, *args, **kwargs):
    response = finalize_response(request, response, *args, **kwargs)
    response.data = dict(
        status=response.status_code,
        msg=response.status_text,
        result=response.data,
    )
    return response


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


def update_query_params(request, form):
    """
    透過form的方式來清理輸入的資料
    :param request:
    :param form:
    :return:
    """
    form = form(request.query_params)
    if form.is_valid():
        request.query_params._mutable = True
        clean_data = {k: v for k, v in form.clean().items() if v != "" and v is not None and k in form.data.keys()}
        request.query_params.clear()
        request.query_params.update(clean_data)
    else:
        return form.errors


class CustomModelViewSet(viewsets.ModelViewSet):
    # 如果有特殊的刪除需求，再進行override
    def destroy(self, request, *args, **kwargs):
        create_by = request.user
        instance = self.get_object()
        
        if hasattr(instance, 'create_by') and create_by != instance.create_by:
            return Response(error_msg.CREATE_BY_NOT_CORRECT, status=status.HTTP_400_BAD_REQUEST)
        
        return super().destroy(request, *args, **kwargs)
    
    def finalize_response(self, request, response, *args, **kwargs):
        return common_finalize_response(super().finalize_response, request, response, *args, **kwargs)
