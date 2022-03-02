from .base import *


# 把 debug 模式關掉。
DEBUG = env('DEBUG')

# 設定 secret key。
SECRET_KEY = env('SECRET_KEY')

# 尊重 HTTPS 連線中的 "X-Forwarded-Proto" header。
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CORS_ALLOW_ALL_ORIGINS = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

STATIC_URL = os.environ.get('STATIC_URL', 'static/')
STATIC_ROOT = 'static/'

GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')
GS_LOCATION = 'upload'
if GS_BUCKET_NAME:
    from google.oauth2 import service_account
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        "/gs/google_secret.json"
    )
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_AUTO_CREATE_ACL = os.getenv('GS_AUTO_CREATE_ACL', 'publicRead')
    GS_DEFAULT_ACL = os.getenv('GS_DEFAULT_ACL', 'publicRead')
    GS_CUSTOM_ENDPOINT = os.getenv('GS_CUSTOM_ENDPOINT', None)

