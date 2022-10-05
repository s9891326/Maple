from .base import *
# import dj_database_url
#
# DATABASES = {}
# DATABASES["default"] = dj_database_url.config(conn_max_age=600)

ROOT_URLCONF = "Maple.urls"
CORS_ALLOW_ALL_ORIGINS = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

import django_heroku

django_heroku.settings(locals(), allowed_hosts=False, secret_key=False)
