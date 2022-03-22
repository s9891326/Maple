from django.contrib.auth.models import User
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import serializers

from Maple.settings.base import SOCIAL_GOOGLE_CLIENT_ID
from accounts.models import SocialAccount


class SocialLoginSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    line_id = serializers.CharField(required=True)
    
    def verify_token(self, token):
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
        id_info = self.verify_token(validated_data.get('token'))
        
        # todo: line id進行驗證是否有該ID
        line_id = validated_data.get('line_id')
        
        # User not exists => create new user
        if not SocialAccount.objects.filter(unique_id=id_info["sub"]).exists():
            user = User.objects.create_user(
                username=f"{id_info['name']} {id_info['email']}",  # Username has to be unique
                first_name=id_info['given_name'],
                last_name=id_info['family_name'],
                email=id_info['email']
            )
            SocialAccount.objects.create(
                user=user,
                line_id=line_id,
                unique_id=id_info['sub']
            )
            return user
        else:
            social_account = SocialAccount.objects.get(unique_id=id_info["sub"])
            return social_account.user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ["username", "email", "first_name", "last_name"]
