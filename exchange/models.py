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
        Weapon = 'weapon', '武器'
        Armor = 'armor', '防具'
        Skins = 'skins', '造型'
        Consumables = 'consumables', '消耗品'
        Cooperate = 'cooperate', '合作'
    
    category = models.CharField(verbose_name="類別", max_length=16,
                                choices=Category.choices, default=Category.Weapon)
    type = models.CharField(verbose_name="種類", max_length=16)
    name = models.CharField(verbose_name="裝備名稱", max_length=16)
    
    class Meta:
        unique_together = ("category", "type", "name")
        verbose_name = verbose_name_plural = "裝備庫"
    
    def __str__(self):
        return f"{self.category},{self.type},{self.name}"


class Equip(models.Model):
    class Stage(models.TextChoices):
        White = 'white', '普通'
        Blue = 'blue', '稀有'
        Purple = 'purple', '史詩'
        Gold = 'gold', '罕見'
        Green = 'green', '傳說'
        Red = 'red', '神話'
        DarkBlue = 'darkBlue', '古代'
        DeadBlue = 'deadBlue', '死靈'
    
    name = models.ForeignKey(EquipLibrary, verbose_name="裝備名稱",
                             on_delete=models.CASCADE, related_name="equip")
    stage_level = models.CharField(verbose_name="階段等級", blank=True, max_length=16,
                                   choices=Stage.choices, default=Stage.White)
    images = models.ImageField(verbose_name="裝備圖片", upload_to=path_and_rename, null=True, blank=True)
    price = models.BigIntegerField(verbose_name="價錢")
    explanation = models.TextField(verbose_name="說明", blank=True, default="")
    create_date = models.DateTimeField(verbose_name="上架日期", auto_now_add=True)
    
    # create_by = models.ForeignKey(User)
    
    class Meta:
        verbose_name = verbose_name_plural = "裝備"
    
    def __str__(self):
        return f"{self.name}"

# class Exchange(models.Model):
#     class Stage(models.TextChoices):
#         White = 'white', '普通'
#         Blue = 'blue', '稀有'
#         Purple = 'purple', '史詩'
#         Gold = 'gold', '罕見'
#         Green = 'green', '傳說'
#         Red = 'red', '神話'
#         DarkBlue = 'darkBlue', '古代'
#         DeadBlue = 'deadBlue', '死靈'
#
#     equip_name = models.CharField(verbose_name="裝備名稱", max_length=16)
#     equip_occupation = models.CharField(verbose_name="裝備職業")
#     # describe = models.TextField(verbose_name="裝備描述", blank=True, null=True, default=None)
#     stage_level = models.CharField(verbose_name="階段等級", blank=True, null=True,
#                                    choices=Stage.choices, default=Stage.White)
#     min_price = models.IntegerField(verbose_name="裝備最低價", default=0)
#     max_price = models.IntegerField(verbose_name="裝備最高價", default=0)
#     count = models.IntegerField(verbose_name="裝備數量", default=0)
#
#     class Meta:
#         verbose_name = verbose_name_plural = "交易所"
#
#     def __str__(self):
#         return ""
