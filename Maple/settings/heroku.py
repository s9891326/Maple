from .base import *


# 尊重 HTTPS 連線中的 "X-Forwarded-Proto" header。
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ORIGIN_WHITELIST = (
#     'http://localhost:8080',
#     'http://localhost:63342',
# )

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

import django_heroku

django_heroku.settings(locals(), databases=False, allowed_hosts=False, secret_key=False)
