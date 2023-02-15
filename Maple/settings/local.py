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

if DEBUG and DEBUG.lower() == "true":
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

MAIN_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/main.log")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'main_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': MAIN_LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 500,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['console', 'main_file'],
            'level': 'WARNING',
            'propagate': False
        },
    }
}
