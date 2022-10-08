from django.db import models

from accounts.models import CustomUser


class Coin(models.Model):
    title = models.CharField(verbose_name="標題", max_length=32)
    value = models.IntegerField(verbose_name="幣值(1億楓幣:多少台幣)")
    total = models.IntegerField(verbose_name="總額(x億楓幣)")
    server_name = models.CharField(verbose_name='伺服器', max_length=8,
                                   choices=CustomUser.ServerName.get_valid_server_name())
    create_by = models.ForeignKey(CustomUser, verbose_name="創建者", on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="上架日期", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="更新日期", auto_now=True)
    
    class Meta:
        verbose_name = verbose_name_plural = "楓幣"
    
    def __str__(self):
        return self.title

