from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from exchange import views

app_name = "exchange"

router = routers.DefaultRouter(trailing_slash=False)
router.register("equip-library", views.EquipLibraryViewSet, basename="equip_library_api")
router.register("equip", views.EquipViewSet, basename="equip_api")

urlpatterns = [
    path('', include(router.urls)),
    # path('equip', views.EquipView.as_view(), name="equip_api"),
]

urlpatterns = [path(r'api/', include(urlpatterns))]
