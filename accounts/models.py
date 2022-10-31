from django.contrib.auth.models import UserManager, AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from utils.util import PathAndRename

USERNAME_MIN_LENGTH = 6
USERNAME_MAX_LENGTH = 30
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 30

game_image_path = PathAndRename("game_images")

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
    phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(verbose_name='手機', validators=[phone_regex], max_length=16,
                             blank=True, null=True, unique=True)
    sms_code = models.IntegerField(verbose_name='驗證號碼', default=0)
    game_name = models.CharField(verbose_name='遊戲名稱', max_length=32, blank=True, null=True, unique=True)
    game_image = models.ImageField(verbose_name='遊戲截圖', upload_to=game_image_path, blank=True)
    is_valid = models.BooleanField(verbose_name='遊戲截圖是否驗證', default=False)
    
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = verbose_name_plural = "客製用戶"
    
    def __str__(self):
        return f"{self.username}"
