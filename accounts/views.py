from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import CustomUser
from accounts.serializer import ThreePartySerializer, CustomUserSerializer
from utils.util import common_finalize_response, CustomModelViewSet


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
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED)
    
    def finalize_response(self, request, response, *args, **kwargs):
        return common_finalize_response(super().finalize_response, request, response, *args, **kwargs)


class CustomUserView(CustomModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        """
        改成只取回特定用戶
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def get_object(self):
        """
        更改partial_update抓instance的方式 改成從JWT token裡面抓
        :return:
        """
        return self.request.user
    
    def destroy(self, request, *args, **kwargs):
        # return Response("Delete method is not offered in this path.", status=status.HTTP_403_FORBIDDEN)
        return Response("Delete method不允許被使用", status=status.HTTP_403_FORBIDDEN)
