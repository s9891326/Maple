from django.contrib.auth import get_user, authenticate
from django.contrib.auth.middleware import AuthenticationMiddleware
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializer import ThreePartySerializer, CustomUserSerializer
from utils.response import common_finalize_response


def get_tokens_for_user(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return dict(
        refresh=str(refresh),
        access=str(refresh.access_token)
    )


class ThreePartyLogin(TokenObtainPairView):
    serializer_class = ThreePartySerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = serializer.save()
            except Exception as e:
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
            return Response(get_tokens_for_user(user))
        else:
            raise Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def finalize_response(self, request, response, *args, **kwargs):
        return common_finalize_response(super().finalize_response, request, response, *args, **kwargs)


class CustomUserView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()
    
    def get_queryset(self):
        return [self.request.user]

    def finalize_response(self, request, response, *args, **kwargs):
        return common_finalize_response(super().finalize_response, request, response, *args, **kwargs)
