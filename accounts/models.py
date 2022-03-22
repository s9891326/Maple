from django.contrib.auth.models import User
from django.db import models


class SocialAccount(models.Model):
    provider = models.CharField(max_length=16, default='google')  # 若未來新增其他的登入方式,如Facebook,GitHub...
    unique_id = models.CharField(max_length=64, unique=True)
    line_id = models.CharField(max_length=64)
    user = models.ForeignKey(User, related_name='social', on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = "社群用戶"

    def __str__(self):
        return f"{self.user.username}"
