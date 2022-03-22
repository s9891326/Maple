from django.urls import path, include
from rest_framework import routers

from exchange import views

app_name = "exchange"

router = routers.DefaultRouter(trailing_slash=False)
router.register("product-list", views.ProductListViewSet, basename="product_list_api")
router.register("product", views.ProductViewSet, basename="product_api")

urlpatterns = [
    path('/', include(router.urls)),
    # path('equip', views.EquipView.as_view(), name="equip_api"),
]

# urlpatterns = [path(r'api/', include(urlpatterns))]
