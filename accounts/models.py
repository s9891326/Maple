from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Provider(models.TextChoices):
        Null = '無', '無'
        Google = 'Google', 'Google'
    
    # 若未來新增其他的登入方式,如Facebook,GitHub...
    provider = models.CharField(verbose_name='註冊方式', max_length=16,
                                choices=Provider.choices, default=Provider.Null)
    unique_id = models.CharField(verbose_name='第三方辨識碼', max_length=64, unique=True)
    line_id = models.CharField(verbose_name='line id', max_length=64)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = verbose_name_plural = "客製用戶"

    def __str__(self):
        return f"{self.username}"
