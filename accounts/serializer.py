from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import serializers

from Maple.settings.base import SOCIAL_GOOGLE_CLIENT_ID
from accounts.models import CustomUser, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH, PASSWORD_MIN_LENGTH, \
    PASSWORD_MAX_LENGTH
from utils import error_msg


class ThreePartySerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=CustomUser.Provider, required=True)
    token = serializers.CharField(required=True)
    
    @staticmethod
    def verify_token(token):
        """
        驗證 id_token 是否正確
        token: JWT
        """
        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), SOCIAL_GOOGLE_CLIENT_ID)
        except Exception as e:
            raise e
        
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        if id_info['aud'] not in [SOCIAL_GOOGLE_CLIENT_ID]:
            raise ValueError('Could not verify audience.')
        
        return id_info
    
    def create(self, validated_data):
        type = validated_data.get("type")
        
        id_info = None
        if type == CustomUser.Provider.Google:
            id_info = self.verify_token(validated_data.get('token'))
        
        # User not exists => create new user
        if not CustomUser.objects.filter(unique_id=id_info["sub"]).exists():
            user = CustomUser.objects.create_user(
                username=f"{id_info['name']} {id_info['email']}",  # Username has to be unique
                first_name=id_info['name'],
                email=id_info['email'],
                unique_id=id_info['sub'],
                provider=CustomUser.Provider.Google,
            )
            
            return user
        else:
            return CustomUser.objects.get(unique_id=id_info["sub"])


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="first_name")
    password2 = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(style={"input_type": "password"}, required=False, write_only=True)
    new_password2 = serializers.CharField(style={"input_type": "password"}, required=False, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'provider', 'contact',
            'password', 'password2', 'new_password', 'new_password2', 'server_name'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
        }
    
    def to_representation(self, instance):
        """
        改變序列化的輸出內容，增加額外的數據
        :param instance:
        :return:
        """
        representation = super(CustomUserSerializer, self).to_representation(instance)
        representation["server_name"] = instance.get_server_name_display()
        return representation
    
    def create(self, validated_data):
        """
        提供登入 + 註冊功能
        登入: username、password
        註冊: username、password、password2、email
        :param validated_data:
        :return:
        """
        username = validated_data['first_name']
        password = validated_data['password']
        password2 = validated_data.get("password2")
        
        # If have password2 go register, else go login.
        if password2:
            # 驗證帳號、密碼長度限制
            length_limit_validation(username, "username", USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH)
            length_limit_validation(password, "password", PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)
            
            # 重複密碼跟密碼不一樣
            if password != password2:
                raise serializers.ValidationError(error_msg.PASSWORD_NOT_MATCH)
            
            if not CustomUser.objects.filter(username=username).exists():
                try:
                    user = CustomUser.objects.create_user(
                        username=username,
                        first_name=validated_data['first_name'],
                        email=validated_data['email'],
                        password=password
                    )
                except Exception as e:
                    raise serializers.ValidationError(error_msg.CREATE_USER_ARGS_NOT_FOUND % e.args[0])
            else:
                # 重複的使用者ID
                raise serializers.ValidationError(error_msg.USER_ALREADY_EXISTS)
        else:
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(error_msg.DONT_HAVE_THIS_USER)
            if not user.check_password(password):
                raise serializers.ValidationError(error_msg.PASSWORD_NOT_CORRECT)
        return user
    
    def update(self, instance, validated_data):
        """
        更新用戶資訊
        :param instance:
        :param validated_data:
        :return:
        """
        new_password = validated_data.get("new_password")
        new_password2 = validated_data.get("new_password2")
        user = self.context["request"].user
        
        if new_password and new_password2:
            length_limit_validation(new_password, "password", PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)
            user.set_password(new_password)
            user.save()
        
        # google登入的用戶不能修正email
        if user.provider == CustomUser.Provider.Google.value:
            validated_data.pop("email", None)
        
        # 清除帳號、密碼欄位的修正
        validated_data.pop("username", None)
        validated_data.pop("password", None)
        validated_data.pop("new_password", None)
        validated_data.pop("new_password2", None)
        
        return super().update(instance, validated_data)


class CustomUserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('contact',)


def length_limit_validation(value, value_name, min_length, max_length):
    """
    長度限制驗證器
    :param value:
    :param value_name:
    :param min_length:
    :param max_length:
    :return:
    """
    if len(value) < min_length or len(value) > max_length:
        raise serializers.ValidationError(error_msg.LENGTH_EXCEEDS_LIMIT % (value_name, min_length, max_length))
