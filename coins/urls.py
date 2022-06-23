from django.urls import path, include
from rest_framework import routers

from coins import views

app_name = "coins"

router = routers.DefaultRouter(trailing_slash=False)
router.register("coin", views.CoinViewSet, basename="coin_api")

urlpatterns = [
    path('', include(router.urls)),
]

