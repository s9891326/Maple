from django.db import transaction
from rest_framework import serializers

from exchange.models import EquipLibrary, Equip, EquipImage


class EquipLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipLibrary
        fields = '__all__'


class EquipImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipImage
        fields = ('id', 'image', )


class EquipSerializer(serializers.ModelSerializer):
    images = EquipImageSerializer(source="equipimage_set", many=True, required=False)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    
    class Meta:
        model = Equip
        fields = '__all__'

    def to_representation(self, instance):
        """
        改變序列化的輸出內容，增加額外的數據 => 不影響post method輸入equip_library = id
        :param instance:
        :return:
        """
        self.fields['equip_library'] = EquipLibrarySerializer(read_only=True)
        return super(EquipSerializer, self).to_representation(instance)

    @transaction.atomic
    def create(self, validated_data):
        # https://stackoverflow.com/questions/48756249/django-rest-uploading-and-serializing-multiple-images
        images_data = self.context.get('view').request.FILES
        equip = Equip.objects.create(**validated_data)
        for image_data in images_data.getlist("images"):
            EquipImage.objects.create(equip=equip, image=image_data)

        # 幫裝備庫增加對應的最大最小價格
        equip_library_id = validated_data["equip_library"].id
        price = validated_data["price"]
        EquipLibrary.objects.filter(pk=equip_library_id, min_price__gt=price).update(min_price=price)
        EquipLibrary.objects.filter(pk=equip_library_id, max_price__lt=price).update(max_price=price)
        return equip
