# Docker 部屬Django教學

- [Django + Uwsgi(單容器)](https://zhuanlan.zhihu.com/p/141976805)
- [Django + Uwsgi + Nginx](https://blog.csdn.net/weixin_42134789/article/details/106205182)
- [Django + Uwsgi + Nginx + Redis + Mysql](https://zhuanlan.zhihu.com/p/145364353)

docker run -it --name mysite3 -p 8000:8000 \
-v /data/code/django_deploy:/var/www/html/django_deploy \
-d django_mysite_img:v1


docker run -it -p 8080:8080 --name mysite-nginx \
-v /data/code/django_deploy/static:/usr/share/nginx/html/static \
-v /data/code/django_deploy/media:/usr/share/nginx/html/media \
-v /data/code/django_deploy/compose/nginx/log:/var/log/nginx \
-d mynginx:v1


- 在部屬環境中，請自行增加`.env`檔案
```
DEBUG=True
```

- docker-compose
```
# 进入docker-compose.yml所在文件夹，输入以下命令构建镜像
sudo docker-compose build
# 查看已生成的镜像
sudo docker images
# 启动容器组服务
sudo docker-compose up
# 查看运行中的容器
sudo docker ps
```

- 增加gitignore
```buildoutcfg
curl https://www.toptal.com/developers/gitignore/api/python,pycharm+all,django > .gitignore
```

# 引用套件
- [django-simple-UI](https://simpleui.72wo.com/docs/simpleui/doc.html#%E4%BB%8B%E7%BB%8D)
- [django-simple-history](https://django-simple-history.readthedocs.io/en/latest/)
