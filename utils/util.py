import os
import shutil
from pathlib import Path

from Maple.settings.base import MEDIA_ROOT, STATIC_ROOT


def extract_dataset_by_folder(from_folder: str, to_folder: str):
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
            image_rename = f"{i}_{k}.jpg"
            image_path = f"{to_folder}/{image_rename}"
            shutil.copyfile(Path(folder_path, image), Path(to_directory, image_rename))
            data[image_name] = image_path
        dataset[data_category[category_num]].append({data_type[data_type_index]: data})
        data_type_index += 1
    
    return dataset