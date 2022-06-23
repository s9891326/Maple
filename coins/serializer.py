from rest_framework import serializers

from coins.models import Coin


class CoinSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    create_by = serializers.StringRelatedField()
    
    class Meta:
        model = Coin
        fields = '__all__'
    
    def to_representation(self, instance):
        """
        改變序列化的輸出內容，增加額外的數據
        :param instance:
        :return:
        """
        representation = super(CoinSerializer, self).to_representation(instance)
        representation["contact_method"] = instance.get_contact_method_display()
        representation["server_name"] = instance.get_server_name_display()
        return representation
        
    def create(self, validated_data):
        req = self.context.get('view').request
        create_by = req.user
        return Coin.objects.create(**validated_data, create_by=create_by)

