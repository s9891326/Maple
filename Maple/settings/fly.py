import dj_database_url

DATABASES = {}
DATABASES["default"] = dj_database_url.config(conn_max_age=600)

CORS_ALLOW_ALL_ORIGINS = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
