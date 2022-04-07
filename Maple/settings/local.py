from .base import *


db_host = "mysql"
redis = "redis"
db_port = "3306"
db_name = env("DB_NAME", "maple")
db_user = env("DB_USER", "dbuser")
db_password = env("DB_PASSWORD", "riu405405")
if DEBUG:
    if DEBUG.lower() == "true":
        db_host = redis = "192.168.223.127"
        db_port = "3305"
    else:
        db_host = redis = "127.0.0.1"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,  # 使用docker時這裡使用的是DB的別名，docker會自動解析成IP
        'PORT': db_port,
    }
}
