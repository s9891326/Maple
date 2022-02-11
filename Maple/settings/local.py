import environ

from .base import *

SECRET_KEY = 'django-insecure-m3mfow6@_g6#g10%4*9mzgl9v^m6f@g%+#ue404c7@bnjtw47('

ROOT_DIR = (environ.Path(__file__) - 3)
# print(f"Root dir: {ROOT_DIR}")
env = environ.Env()
env.read_env(str(ROOT_DIR.path(".env")))
DEBUG = env("DEBUG")

mysql = "mysql"
redis = "redis"
if DEBUG:
    mysql = redis = "192.168.223.127"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',  # 数据库名
        'USER': 'dbuser',  # 你设置的用户名 - 非root用户
        'PASSWORD': 'riu405405',  # # 换成你自己密码
        'HOST': mysql,  # 注意：这里使用的是db别名，docker会自动解析成ip
        'PORT': '3305',  # 端口
    }
}
