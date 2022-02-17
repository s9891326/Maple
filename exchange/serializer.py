from django.db import transaction
from rest_framework import serializers

from exchange.models import ProductList, Product, ProductImage


class ProductListSerializer(serializers.ModelSerializer):
    zh_stage_level = serializers.ReadOnlyField(source="get_stage_level_display")

    class Meta:
        model = ProductList
        fields = '__all__'
    
    # def to_representation(self, instance):
    #     two_days_ago = timezone.now() - timezone.timedelta(days=2)
    #     data = super().to_representation(instance)
    #     product = Product.objects.filter(
    #         product_list__pk=data["product_list_id"], create_date__gte=two_days_ago
    #     )
    #     data["count"] = product.count()
    #     min_price = max_price = 0
    #     if product:
    #         min_price = product.first().price
    #         max_price = product.last().price
    #     data["min_price"] = min_price
    #     data["max_price"] = max_price
    #     # data["product"] = ProductSerializer(product.all(), many=True).data
    #
    #     return data


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('product_image_id', 'image',)


class ProductSerializer(serializers.ModelSerializer):
    # images = ProductImageSerializer(source="product_image", many=True, required=False)
    images = serializers.SerializerMethodField(read_only=True, required=False)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    # product_list_image = serializers.SerializerMethodField(read_only=True, required=False)
    # product_list_name = serializers.CharField(source="product_list.name", read_only=True, required=False)
    product_list_data = ProductListSerializer(source="product_list", read_only=True, required=False)
    
    class Meta:
        model = Product
        fields = '__all__'
    
    # def to_representation(self, instance):
    #     """
    #     改變序列化的輸出內容，增加額外的數據 => 不影響post method輸入equip_library = id
    #     :param instance:
    #     :return:
    #     """
    #     self.fields['equip_library'] = EquipLibrarySerializer(read_only=True)
    #     return super(ProductSerializer, self).to_representation(instance)
    
    @transaction.atomic
    def create(self, validated_data):
        # https://stackoverflow.com/questions/48756249/django-rest-uploading-and-serializing-multiple-images
        images_data = self.context.get('view').request.FILES
        product = Product.objects.create(**validated_data)
        for image_data in images_data.getlist("images"):
            ProductImage.objects.create(product=product, image=image_data)
        return product
    
    def get_product_list_image(self, obj):
        request = self.context.get('request', None)
        url = obj.product_list.image.url
        if request is not None:
            return request.build_absolute_uri(url)
        return url
    
    def get_images(self, obj):
        request = self.context.get('request', None)
        images = obj.product_image.all().values_list("image", flat=True)
        if request is not None:
            return [request.build_absolute_uri(image) for image in images]
        return [image for image in images]
    
    # @staticmethod
    # def setup_eager_loading(queryset):
    #     """
    #     提供view快速載入DB內各表之間的關聯(1 -> *、* -> 1)
    #     :param queryset:
    #     :return:
    #     """
    #     queryset = queryset.prefetch_related("product_image")
    #     return queryset
