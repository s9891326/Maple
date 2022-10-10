from django.db import transaction
from rest_framework import serializers

from accounts.serializer import CustomUserContactSerializer
from exchange.models import ProductList, Product, ProductImage
from storages.google import CUSTOM_GCS, CUSTOM_GCS_CLIENT
from utils import error_msg


class ProductListSerializer(serializers.ModelSerializer):
    zh_stage_level = serializers.ReadOnlyField(source="get_stage_level_display")
    
    class Meta:
        model = ProductList
        fields = '__all__'
    
    def to_representation(self, instance):
        """
        :param instance:
        :return:
        """
        representation = super(ProductListSerializer, self).to_representation(instance)
        representation["category"] = instance.get_category_display()
        representation["career"] = instance.get_career_display()
        return representation


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('product_image_id', 'image',)


class ProductSerializer(serializers.ModelSerializer):
    # images = ProductImageSerializer(source="product_image", many=True, required=False)
    images = serializers.SerializerMethodField(read_only=True, required=False)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    # product_list_image = serializers.SerializerMethodField(read_only=True, required=False)
    # product_list_name = serializers.CharField(source="product_list.name", read_only=True, required=False)
    product_list_data = ProductListSerializer(source="product_list", read_only=True, required=False)
    create_by = CustomUserContactSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        """
        改變序列化的輸出內容，增加額外的數據
        :param instance:
        :return:
        """
        representation = super(ProductSerializer, self).to_representation(instance)
        representation["potential_capability"] = [s.replace(" ", "") for s in representation["potential_capability"].split(",")]
        representation["spark_capability"] = [s.replace(" ", "") for s in representation["spark_capability"].split(",")]
        representation["potential_level"] = instance.get_potential_level_display()
        representation["spark_level"] = instance.get_spark_level_display()
        representation["maple_capability"] = instance.get_maple_capability_display()
        representation["server_name"] = instance.get_server_name_display()
        return representation
    
    @transaction.atomic
    def create(self, validated_data):
        # https://stackoverflow.com/questions/48756249/django-rest-uploading-and-serializing-multiple-images
        req = self.context.get('view').request
        images_data = req.FILES
        create_by = req.user
        product = Product.objects.create(**validated_data, create_by=create_by)
        for image_data in images_data.getlist("images"):
            ProductImage.objects.create(product=product, image=image_data)
        return product
    
    def get_product_list_image(self, obj):
        request = self.context.get('request', None)
        url = obj.product_list.image.url
        if request is not None:
            if CUSTOM_GCS_CLIENT:
                return CUSTOM_GCS.url(url)
            return request.build_absolute_uri(url)
        return url
    
    def get_images(self, obj):
        request = self.context.get('request', None)
        images = obj.product_image.all().values_list("image", flat=True)
        if request is not None:
            if CUSTOM_GCS_CLIENT:
                return [CUSTOM_GCS.url(image) for image in images]
            return [request.build_absolute_uri(image) for image in images]
        return [image for image in images]

    def update(self, instance, validated_data):
        create_by = self.context["request"].user
        
        if create_by != instance.create_by:
            raise serializers.ValidationError(error_msg.CREATE_BY_NOT_CORRECT)
        
        # 不能被更改的欄位
        validated_data.pop("product_list", None)
        validated_data.pop("create_by", None)
        
        return super().update(instance, validated_data)

    # @staticmethod
    # def setup_eager_loading(queryset):
    #     """
    #     提供view快速載入DB內各表之間的關聯(1 -> *、* -> 1)
    #     :param queryset:
    #     :return:
    #     """
    #     queryset = queryset.prefetch_related("product_image")
    #     return queryset
