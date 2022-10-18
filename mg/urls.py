from django.urls import path

from mg import views

app_name = "mg"

urlpatterns = [
    path('test', views.test, name="test"),
    path('add-product-list', views.add_product_list, name="add_product_list"),
    path('delete-product-list', views.delete_product_list, name="delete_product_list"),
    path('add-product', views.add_product, name="add_product"),
    path('upload-image', views.upload_image_to_gcp_storage, name="upload_image")
]
