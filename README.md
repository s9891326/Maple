# Docker 部屬Django教學

- [Django + Uwsgi(單容器)](https://zhuanlan.zhihu.com/p/141976805)
- [Django + Uwsgi + Nginx](https://blog.csdn.net/weixin_42134789/article/details/106205182)
- [Django + Uwsgi + Nginx + Redis + Mysql](https://zhuanlan.zhihu.com/p/145364353)

docker run -it --name mysite3 -p 8000:8000 \
-v /data/code/maple:/var/Maple \
-d django_mysite_img:v1


docker run -it -p 8080:8080 --name mysite-nginx \
-v /data/code/maple/static:/usr/share/nginx/html/static \
-v /data/code/maple/media:/usr/share/nginx/html/media \
-v /data/code/maple/compose/nginx/log:/var/log/nginx \
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
sudo docker-compose up -d
# 查看运行中的容器
sudo docker ps
# 移除none images
docker rmi $(docker images -f "dangling=true" -q)
```


- Makefile
```
建議搭配著linux中的zsh-autoswitch_virtualenv使用
mkvenv --python=$(which python3.7) --把該專案設定成指定的python版本
```

- 增加gitignore
```
curl https://www.toptal.com/developers/gitignore/api/python,pycharm+all,django > .gitignore
```

- 把.env檔新增到heroku config內
```
heroku config:set $(cat .env | sed '/^$/d; /#[[:print:]]*$/d')
```

# 引用套件
- [django-simple-UI](https://simpleui.72wo.com/docs/simpleui/doc.html#%E4%BB%8B%E7%BB%8D)
- [django-simple-history](https://django-simple-history.readthedocs.io/en/latest/)
