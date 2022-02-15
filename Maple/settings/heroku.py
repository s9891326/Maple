
from .base import *

from django.core.exceptions import ImproperlyConfigured


def env(key):
    try:
        return os.environ.get(key)
    except KeyError:
        raise ImproperlyConfigured(
            'Environment variable {key} required.'.format(key=key)
        )


# 把 debug 模式關掉。
DEBUG = env('DEBUG')

# 設定 secret key。
SECRET_KEY = env('SECRET_KEY')

# 尊重 HTTPS 連線中的 "X-Forwarded-Proto" header。
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CORS header
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',  # localhost:63342 != 127.0.0.1:63342
    'http://localhost:63342',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}
