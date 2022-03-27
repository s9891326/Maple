from django.contrib.auth.models import User
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import serializers

from Maple.settings.base import SOCIAL_GOOGLE_CLIENT_ID
from accounts.models import CustomUser


class ThreePartySerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    line_id = serializers.CharField(required=False)
    
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
        create_func = None
        if type == "google":
            id_info = self.verify_token(validated_data.get('token'))
            create_func = self.create_user_from_google
        
        if not id_info:
            # custom create user
            pass
        if not CustomUser.objects.filter(unique_id=id_info["sub"]).exists():
            # User not exists => create new user
            return create_func(validated_data, id_info)
        else:
            return CustomUser.objects.get(unique_id=id_info["sub"])
    
    @staticmethod
    def create_user_from_google(validated_data, id_info):
        # todo: line id進行驗證是否有該ID
        line_id = validated_data.get('line_id')
        if not line_id:
            raise ValueError("line_id is not current.")
        
        user = CustomUser.objects.create_user(
            username=f"{id_info['name']} {id_info['email']}",  # Username has to be unique
            first_name=id_info['name'],
            email=id_info['email'],
            line_id=line_id,
            unique_id=id_info['sub'],
            provider=CustomUser.Provider.Google,
        )
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="first_name")
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'provider', 'line_id')
