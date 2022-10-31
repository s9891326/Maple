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


# --START--set file storage-- #
# 將Django預設檔案存取Class設定使用django_gcloud_storage
# DEFAULT_FILE_STORAGE = 'django_gcloud_storage.DjangoGCloudStorage'
DEFAULT_FILE_STORAGE = 'storages.google.CustomGCS'

# 設定你的Google Cloud Storage Project名稱
GCS_PROJECT = "maple-storage"

# 設定檔案存放的Bucket名稱
GCS_BUCKET = "maple-storage"

# 設定你的金鑰JSON Path
# 必須是是本機的絕對路徑
# GCS_CREDENTIALS_FILE_PATH = BASE_DIR / "maple-storage-da84838b377e.json"
GCS_CREDENTIALS = env('GCS_CREDENTIALS')
# --END--set file storage-- #

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
