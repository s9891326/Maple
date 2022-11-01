import datetime
import random

from data_spec_validator.decorator import dsv
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView

import config
from accounts.models import CustomUser
from accounts.serializer import ThreePartySerializer, CustomUserSerializer
from config import redis_config
from utils import error_msg
from utils.http_util import return_jsonify, jsonify
from utils.params_spec_util import SendCodeSpec
from utils.redis_util import rds
from utils.sms_util import twilio_service
from utils.util import common_finalize_response, CustomModelViewSet, until_midnight_timestamp


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


@api_view(('POST',))
@return_jsonify
@dsv(SendCodeSpec)
def send_code(request):
    """
    寄送簡訊
    phone: +886912345678
    client_ip: ipv4
    :param request:
    :return:
    """
    user = request.user
    phone = request.POST.get("phone")
    client_ip = request.POST.get("client_ip")
    
    if (rds.zscore(redis_config.SEND_CODE_KEY, client_ip) or 0) >= config.EXCEED_SEND_CODE_LIMIT:
        return jsonify(msg="Warning", results=error_msg.EXCEED_SEND_CODE_LIMIT % config.EXCEED_SEND_CODE_LIMIT)
    
    code = random.randint(100000, 999999)
    result = twilio_service.send_code(phone, str(code))
    
    if result:
        user.sms_code = code
        user.save()
        
        rds.zincrby(redis_config.SEND_CODE_KEY, client_ip, 1)
        rds.expire(redis_config.SEND_CODE_KEY, until_midnight_timestamp())
        print(rds.ttl(redis_config.SEND_CODE_KEY))
    
    return jsonify(results=error_msg.SUCCESS)
