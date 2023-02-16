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
LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': LOG_FORMAT
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'loki': {
            'class': 'django_loki.LokiFormatter',  # required
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] [%(funcName)s] %(message)s',  # optional, default is logging.BASIC_FORMAT
            'datefmt': '%Y-%m-%d %H:%M:%S',  # optional, default is '%Y-%m-%d %H:%M:%S'
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
        'loki': {
            'level': 'DEBUG',  # required
            'class': 'django_loki.LokiHttpHandler',  # required
            'host': '192.168.223.127',  # required, your grafana/Loki server host, e.g:192.168.57.242
            'formatter': 'loki',  # required, loki formatter,
            'port': 3100,  # optional, your grafana/Loki server port, default is 3100
            'timeout': 0.5,  # optional, request Loki-server by http or https time out, default is 0.5
            'protocol': 'http',  # optional, Loki-server protocol, default is http
            'source': 'Loki',  # optional, label name for Loki, default is Loki
            'src_host': 'localhost',  # optional, label name for Loki, default is localhost
            'tz': 'UTC',  # optional, timezone for formatting timestamp, default is UTC, e.g:Asia/Shanghai
        },
    },
    'loggers': {
        'main': {
            'handlers': ['console', 'main_file'],
            'level': 'WARNING',
            'propagate': False
        },
        'loki': {
            'handlers': ['console', 'main_file', 'loki'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
