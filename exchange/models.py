import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):
    
    def __init__(self, sub_path):
        self.path = sub_path
    
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
        return os.path.join(self.path, filename)


path_and_rename = PathAndRename("equip")


class EquipLibrary(models.Model):
    class Category(models.TextChoices):
        Weapon = '武器', '武器'
        Armor = '防具', '防具'
        Skins = '造型', '造型'
        Consumables = '消耗品', '消耗品'
        Cooperate = '合作', '合作'
    
    category = models.CharField(verbose_name="類別", max_length=16,
                                choices=Category.choices, default=Category.Weapon)
    type = models.CharField(verbose_name="種類", max_length=16)
    name = models.CharField(verbose_name="裝備名稱", max_length=16)
    min_price = models.BigIntegerField(verbose_name="最低價錢", default=0)
    max_price = models.BigIntegerField(verbose_name="最高價錢", default=0)
    
    class Meta:
        unique_together = ("category", "type", "name")
        verbose_name = verbose_name_plural = "裝備庫"
    
    def __str__(self):
        return f"{self.category},{self.type},{self.name}"


class Equip(models.Model):
    class Stage(models.TextChoices):
        White = '普通', '普通'
        Blue = '稀有', '稀有'
        Purple = '史詩', '史詩'
        Gold = '罕見', '罕見'
        Green = '傳說', '傳說'
        Red = '神話', '神話'
        DarkBlue = '古代', '古代'
        DeadBlue = '死靈', '死靈'
    
    equip_library = models.ForeignKey(EquipLibrary, verbose_name="裝備庫", on_delete=models.CASCADE)
    stage_level = models.CharField(verbose_name="階段等級", blank=True, max_length=16,
                                   choices=Stage.choices, default=Stage.White)
    price = models.BigIntegerField(verbose_name="價錢")
    explanation = models.TextField(verbose_name="說明", blank=True, default="")
    create_date = models.DateTimeField(verbose_name="上架日期", auto_now_add=True)
    
    # create_by = models.ForeignKey(User)
    
    class Meta:
        verbose_name = verbose_name_plural = "裝備"
    
    def __str__(self):
        return f"{self.equip_library}"


class EquipImage(models.Model):
    equip = models.ForeignKey(Equip, verbose_name="裝備", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="裝備圖片", upload_to=path_and_rename, null=True, blank=True)
    
    class Meta:
        verbose_name = verbose_name_plural = "裝備圖庫"
    
    def __str__(self):
        return f"{self.equip}-{self.image}"
