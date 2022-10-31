from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from accounts import views

app_name = "accounts"

router = routers.DefaultRouter(trailing_slash=False)
router.register("user", views.CustomUserView, basename="user_api")

urlpatterns = [
    path('', include(router.urls)),
    path('three-party-login', views.ThreePartyLogin.as_view(), name="three_party_login_api"),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path('send_code', views.send_code, name="send_sms_code"),
]
