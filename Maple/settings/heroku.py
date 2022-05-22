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
GCS_CREDENTIALS = env('GCS_SERVICE_ACCOUNT')

import django_heroku

django_heroku.settings(locals(), databases=False, allowed_hosts=False, secret_key=False)
