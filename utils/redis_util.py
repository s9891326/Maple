import redis

from Maple.settings import base

if base.DJANGO_SETTINGS_MODULE == base.FLY_MODE:
    from Maple.settings import fly as setting
else:
    from Maple.settings import local as setting

rds = redis.StrictRedis(
    host=setting.redis_host, port=setting.redis_port, password=setting.redis_password
)
