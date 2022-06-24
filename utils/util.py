import json
import os
import shutil
from pathlib import Path

from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from Maple.settings.base import MEDIA_ROOT, STATIC_ROOT
from storages.google import BUCKET
from utils import error_msg

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def extract_dataset_by_folder(from_folder: str, to_folder: str, default_image_path=None):
    from_directory = Path(STATIC_ROOT, from_folder)
    to_directory = Path(MEDIA_ROOT, to_folder)
    
    if not os.path.exists(to_directory):
        os.makedirs(to_directory)
    
    from_directory = list(os.walk(from_directory))
    data_category = from_directory[0][1]
    from_directory_folder = from_directory[1:]
    
    # {
    #     "武器": [
    #         {
    #             "雙手劍": {
    #                 "傑伊西恩雙手劍": "product_list_image_default/0_0.jpg",
    #                 "傑伊西恩雙手劍2": "product_list_image_default/0_0.jpg",
    #             },
    #         },
    #     ]
    # }
    dataset = dict()
    data_type = None
    data_type_index = 0
    category_num = -1
    
    for i, folder in enumerate(from_directory_folder):
        if folder[1]:
            data_type = folder[1]
            data_type_index = 0
            category_num += 1
            dataset[data_category[category_num]] = list()
            continue
        folder_path = folder[0]
        data = dict()
        for k, image in enumerate(folder[2]):
            image_name = image.split(".")[0]
            if default_image_path:
                image_path = default_image_path("", image)
            else:
                image_rename = f"{i}_{k}.jpg"
                image_path = f"{to_folder}/{image_rename}"
                shutil.copyfile(Path(folder_path, image), Path(to_directory, image_rename))
            data[image_name] = image_path
        dataset[data_category[category_num]].append({data_type[data_type_index]: data})
        data_type_index += 1
    
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
