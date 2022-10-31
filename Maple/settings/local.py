from .base import *
import config

db_host = "mysql"
redis_host = "redis"
redis_password = "riu405405"
redis_port = 6380
db_port = "3306"
db_name = env("DB_NAME", "maple")
db_user = env("DB_USER", "dbuser")
db_password = env("DB_PASSWORD", "riu405405")

if DEBUG:
    db_host = redis_host = "192.168.223.127"
    db_port = "3305"
else:
    db_host = redis_host = "127.0.0.1"

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

# 设置redis缓存。这里密码为redis.conf里设置的密码
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{redis_host}:6380",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "riu405405",
        },
    }
}
