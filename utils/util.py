# import os
# import shutil
# from pathlib import Path
# from distutils.dir_util import copy_tree
#
#
# from Maple.settings import BASE_DIR, STATIC_ROOT, MEDIA_ROOT
#
# from_directory = Path(STATIC_ROOT, "images", "product_list")
# to_directory = Path(MEDIA_ROOT, "product_list_image_default")
#
# if not os.path.exists(to_directory):
#     os.makedirs(to_directory)
#
#
# from_directory = list(os.walk(from_directory))
# data_type = from_directory[0][1]
# from_directory_folder = from_directory[1:]
#
# # request = dict(
# #     category=ProductList.Category.Weapon.value,
# #     type="雙手劍",
# #     name="傑伊西恩雙手劍",
# #     stage_level=ProductList.Stage.White.value,
# #     image=
# # )
#
# dataset = dict()
# # {
# #     "雙手劍": {
# #         "傑伊西恩雙手劍": "product_list_image_default/0_0.jpg"
# #     }
# # }
# for i, folder in enumerate(from_directory_folder):
#     folder_name = folder[0]
#     data = dict()
#     for k, image in enumerate(folder[2]):
#         image_name = image.split(".")[0]
#         image_rename = f"{i}_{k}.jpg"
#         image_path = f"product_list_image_default/{image_rename}"
#         shutil.copyfile(Path(folder_name, image), Path(to_directory, image_rename))
#         data[image_name] = image_path
#     dataset[data_type[i]] = data
#     break
#
# print(dataset)
#
