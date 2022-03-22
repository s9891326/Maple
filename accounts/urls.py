from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from accounts.views import GoogleLogin

urlpatterns = [
    path('token/obtain', GoogleLogin.as_view(), name="token_obtain"),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]

