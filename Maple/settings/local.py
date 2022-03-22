from .base import *


mysql = "mysql"
redis = "redis"
port = "3306"
if DEBUG:
    if DEBUG.lower() == "true":
        mysql = redis = "192.168.223.127"
        port = "3305"
    else:
        mysql = redis = "127.0.0.1"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maple',  # 数据库名
        'USER': 'dbuser',  # 你设置的用户名 - 非root用户
        'PASSWORD': 'riu405405',  # # 换成你自己密码
        'HOST': mysql,  # 注意：这里使用的是db别名，docker会自动解析成ip
        'PORT': port,  # 端口
    }
}
