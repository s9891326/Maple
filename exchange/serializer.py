from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from exchange.models import EquipLibrary, Equip, EquipImage


class EquipLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipLibrary
        fields = '__all__'
    
    def to_representation(self, instance):
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        data = super().to_representation(instance)
        equip = Equip.objects.filter(
            equip_library__pk=data["id"], create_date__gte=two_days_ago
        )
        data["count"] = equip.count()
        
        min_price = max_price = 0
        if equip:
            min_price = equip.first().price
            max_price = equip.last().price
        data["min_price"] = min_price
        data["max_price"] = max_price
        
        return data


class EquipImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipImage
        fields = ('id', 'image',)


class EquipSerializer(serializers.ModelSerializer):
    images = EquipImageSerializer(source="equip_image", many=True, required=False)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    
    class Meta:
        model = Equip
        fields = '__all__'
    
    # def to_representation(self, instance):
    #     """
    #     改變序列化的輸出內容，增加額外的數據 => 不影響post method輸入equip_library = id
    #     :param instance:
    #     :return:
    #     """
    #     self.fields['equip_library'] = EquipLibrarySerializer(read_only=True)
    #     return super(EquipSerializer, self).to_representation(instance)
    
    @transaction.atomic
    def create(self, validated_data):
        # https://stackoverflow.com/questions/48756249/django-rest-uploading-and-serializing-multiple-images
        images_data = self.context.get('view').request.FILES
        equip = Equip.objects.create(**validated_data)
        for image_data in images_data.getlist("images"):
            EquipImage.objects.create(equip=equip, image=image_data)
        return equip
    
    @staticmethod
    def setup_eager_loading(queryset):
        """
        提供view快速載入DB內各表之間的關聯(1 -> *、* -> 1)
        :param queryset:
        :return:
        """
        queryset = queryset.prefetch_related("equip_image")
        return queryset
