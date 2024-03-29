import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible

from accounts.models import CustomUser


@deconstructible
class PathAndRename(object):
    
    def __init__(self, sub_path):
        self.path = sub_path
    
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
        return os.path.join(self.path, filename)


product_image_path = PathAndRename("product_image")
product_list_image_path = PathAndRename("product_list_image")


class ProductList(models.Model):
    class Category(models.TextChoices):
        Weapon = 'weapon', '武器'
        Armor = 'armor', '防具'
        Skin = 'skin', '造型'
        Consume = 'consume', '消耗品'
    
    class Stage(models.IntegerChoices):
        White = 0, '普通'
        Blue = 1, '稀有'
        Purple = 2, '史詩'
        Gold = 3, '罕見'
        Green = 4, '傳說'
        Red = 5, '神話'
        DarkBlue = 6, '古代'
    
    class Career(models.TextChoices):
        Null = 'null', '無'
        Share = 'share', '共用'
        Archer = 'archer', '弓箭手'
        Warrior = 'warrior', '劍士'
        Mage = 'mage', '法師'
        Pirate = 'pirate', '海盜'
        Thieves = 'thieves', '盜賊'
    
    product_list_id = models.AutoField(primary_key=True)
    category = models.CharField(verbose_name="類別", max_length=16,
                                choices=Category.choices, default=Category.Weapon)
    type = models.CharField(verbose_name="種類", max_length=16)
    name = models.CharField(verbose_name="裝備名稱", db_index=True, max_length=16)
    stage_level = models.IntegerField(verbose_name="階段等級", choices=Stage.choices, default=Stage.White)
    image = models.ImageField(verbose_name="商品列圖片", upload_to=product_list_image_path, blank=True)
    career = models.CharField(verbose_name="職業", max_length=8,
                              choices=Career.choices, default=Career.Null)
    
    class Meta:
        # Key (category, type, stage_level, name)=(armor, 護肩, 0, 皇家護肩) is duplicated.
        # unique_together = ("category", "type", "stage_level", "name")
        verbose_name = verbose_name_plural = "商品列"
    
    def __str__(self):
        return f"{self.category},{self.type},{self.get_stage_level_display()},{self.name}"


class Product(models.Model):
    class Potential(models.TextChoices):
        Null = 'null', '無'
        Blue = 'blue', '稀有'
        Purple = 'purple', '史詩'
        Gold = 'gold', '罕見'
        Green = 'green', '傳說'
    
    class Spark(models.TextChoices):
        Null = 'null', '無'
        Gold = 'gold', '罕見'
        Green = 'green', '傳說'
        Red = 'red', '神話'
    
    class MapleCapability(models.TextChoices):
        Null = 'null', '無'
        Cruel = 'cruel', '殘忍的紋章'
        Conquer = 'conquer', '征服紋章'
        Clever = 'clever', '機靈紋章'
        Strong = 'strong', '強力紋章'
        Sacred = 'sacred', '神聖紋章'
        Sharp = 'sharp', '銳利紋章'
        Experience = 'experience', '經驗紋章'
        Adjudgement = 'adjudgement', '審判紋章'
        defense = 'defense', '忍耐紋章'
        physical = 'physical', '毀滅紋章'
    
    class Label(models.IntegerChoices):
        Null = 0, '無'
        Special = 1, '特殊'
        Red = 2, '紅色'
        Black = 3, '黑色'
        Master = 4, '大師'
    
    # 必填: star、level、total_level、is_maple、maple_capability、price
    product_id = models.AutoField(primary_key=True)
    product_list = models.ForeignKey(ProductList, verbose_name="商品列", on_delete=models.CASCADE,
                                     related_name="product")
    star = models.IntegerField(verbose_name="星力")
    level = models.IntegerField(verbose_name="裝備等級", default=0)
    total_level = models.IntegerField(verbose_name="裝備總等級", default=0)
    cut_num = models.IntegerField(verbose_name="剩餘剪刀數", blank=True, default=0)
    attack = models.IntegerField(verbose_name="攻擊力", blank=True, default=0)
    main_attribute = models.CharField(verbose_name="主屬性", max_length=16, blank=True, null=True)
    potential_level = models.CharField(verbose_name="淺力等級", max_length=8,
                                       choices=Potential.choices, default=Potential.Null)
    potential_capability = models.CharField(verbose_name="淺力能力", max_length=64, default="")
    spark_level = models.CharField(verbose_name="星火等級", max_length=8,
                                   choices=Spark.choices, default=Spark.Null)
    spark_capability = models.CharField(verbose_name="星火能力", max_length=64, default="")
    is_equippable_soul = models.BooleanField(verbose_name="可裝備靈魂", default=False)
    soul_capability = models.CharField(verbose_name="靈魂能力", max_length=64, blank=True, null=True)
    is_maple = models.BooleanField(verbose_name="是否楓葉底")
    maple_capability = models.CharField(verbose_name="楓底能力", max_length=16,
                                        choices=MapleCapability.choices, default=MapleCapability.Null)
    maple_level = models.IntegerField(verbose_name="楓底等級", default=0)
    price = models.BigIntegerField(verbose_name="價錢", db_index=True)
    explanation = models.TextField(verbose_name="說明", blank=True, default="")
    label_level = models.IntegerField(verbose_name="標籤等級", choices=Label.choices, default=Label.Null)
    create_date = models.DateTimeField(verbose_name="上架日期", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="更新日期", auto_now=True)
    title = models.CharField(verbose_name="商品標題", max_length=32, blank=True, null=True)
    server_name = models.CharField(verbose_name='伺服器', max_length=8,
                                   choices=CustomUser.ServerName.get_valid_server_name())
    create_by = models.ForeignKey(CustomUser, verbose_name="創建者", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = verbose_name_plural = "商品"
    
    def __str__(self):
        return f"{self.product_list}"


class ProductImage(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, verbose_name="商品", on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(verbose_name="商品圖片", upload_to=product_image_path, null=True, blank=True)
    
    class Meta:
        verbose_name = verbose_name_plural = "裝備圖庫"
    
    def __str__(self):
        return f"{self.product}-{self.image}"
