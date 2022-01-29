from django.db import models
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(verbose_name="類別名稱", max_length=8)
    type = models.CharField(verbose_name="類別種類", max_length=16)
    history = HistoricalRecords()

    class Meta:
        unique_together = ("name", "type")
        verbose_name = verbose_name_plural = "類別"
    
    def __str__(self):
        return self.name


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
