from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models

USERNAME_MIN_LENGTH = 6
USERNAME_MAX_LENGTH = 30
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 30


class CustomUser(AbstractUser):
    class Provider(models.TextChoices):
        Null = '無', '無'
        Google = 'google', 'google'
    
    class ServerName(models.TextChoices):
        Null = '無', '無'
        Janis = '傑尼斯', '傑尼斯'
        Scania = '斯卡尼亞', '斯卡尼亞'
        Luna = '露娜', '露娜'
        Vindia = '溫迪亞', '溫迪亞'
        Kainey = '凱伊尼', '凱伊尼'
    
    # 若未來新增其他的登入方式,如Facebook,GitHub...
    provider = models.CharField(verbose_name='註冊方式', max_length=16,
                                choices=Provider.choices, default=Provider.Null)
    unique_id = models.CharField(verbose_name='第三方辨識碼', max_length=64, unique=True, null=True)
    line_id = models.CharField(verbose_name='line id', max_length=64, blank=True, null=True)
    server_name = models.CharField(verbose_name='伺服器', max_length=8,
                                   choices=ServerName.choices, default=ServerName.Null)
    
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = verbose_name_plural = "客製用戶"
    
    def __str__(self):
        return f"{self.username}"
