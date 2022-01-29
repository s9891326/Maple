from django.urls import path, include
from rest_framework import routers

from exchange import views

app_name = "exchange"

router = routers.DefaultRouter()
router.register("category", views.CategoryViewSet, basename="category_api")


urlpatterns = [
    path('', include(router.urls)),
]
