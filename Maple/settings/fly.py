from .base import *
import dj_database_url

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

ROOT_URLCONF = "Maple.urls"
CORS_ALLOW_ALL_ORIGINS = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

redis_host = "fly-maple_redis.upstash.io"
redis_password = env("FLY_REDIS_PASSWORD")
redis_port = 6379

# 设置redis缓存。这里密码为redis.conf里设置的密码
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": f"redis://fly-maple_redis.upstash.io:6379",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "PASSWORD": "0977d11dfedd42f58ab9745fa38e4afe",
#         },
#     }
# }
