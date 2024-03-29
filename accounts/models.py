from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models

USERNAME_MIN_LENGTH = 6
USERNAME_MAX_LENGTH = 30
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 30


class CustomUser(AbstractUser):
    class Provider(models.TextChoices):
        Null = 'null', '無'
        Google = 'google', 'google'
    
    class ServerName(models.TextChoices):
        Null = 'null', '無'
        Janis = 'jenes', '傑尼斯'
        Scania = 'scania', '斯卡尼亞'
        Luna = 'luna', '露娜'
        Vindia = 'vindia', '溫迪亞'
        Kainey = 'kainey', '凱伊尼'
        
        @classmethod
        def get_valid_server_name(cls):
            ret = []
            for e in cls:
                if e == CustomUser.ServerName.Null:
                    continue
                ret.append((e.value, e.label))
            return ret
    
    # 若未來新增其他的登入方式,如Facebook,GitHub...
    provider = models.CharField(verbose_name='註冊方式', max_length=16,
                                choices=Provider.choices, default=Provider.Null)
    unique_id = models.CharField(verbose_name='第三方辨識碼', max_length=64, unique=True, null=True)
    server_name = models.CharField(verbose_name='伺服器', max_length=8,
                                   choices=ServerName.choices, default=ServerName.Null)
    contact = models.JSONField(verbose_name="聯絡方式", null=True)
    
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = verbose_name_plural = "客製用戶"
    
    def __str__(self):
        return f"{self.username}"
