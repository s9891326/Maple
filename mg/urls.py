from django.urls import path

from mg import views

app_name = "mg"

urlpatterns = [
    path('add-product-list', views.add_product_list, name="add_product_list"),
    path('delete-product-list', views.delete_product_list, name="delete_product_list"),
    path('add-product', views.add_product, name="add_product"),
    path('delete-product', views.delete_product, name="delete_product"),
    path('drop-table', views.drop_table, name="drop_table"),
]
