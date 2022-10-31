# Maple API 

### Docker 部屬Django教學

- [Django + Uwsgi(單容器)](https://zhuanlan.zhihu.com/p/141976805)
- [Django + Uwsgi + Nginx](https://blog.csdn.net/weixin_42134789/article/details/106205182)
- [Django + Uwsgi + Nginx + Redis + Mysql](https://zhuanlan.zhihu.com/p/145364353)

```
docker run -it --name mysite3 -p 8000:8000 \
-v /data/code/maple:/var/Maple \
-d django_mysite_img:v1
```

```
docker run -it -p 8080:8080 --name mysite-nginx \
-v /data/code/maple/static:/usr/share/nginx/html/static \
-v /data/code/maple/media:/usr/share/nginx/html/media \
-v /data/code/maple/compose/nginx/log:/var/log/nginx \
-d mynginx:v1
```

- 單純run docker執行maple_web
```
docker build -t maple_web2:v2 .
docker run -it -p 8000:8000 --name maple_web -d maple_web2:v2
docker exec -it maple_web bash
docker exec -it maple_web /bin/bash start.sh
docker exec -it -d maple_web_1 /bin/bash start.sh
```

- 一些基本的操作
```
docker rm -f < Container_ID>
docker rmi -f <Image_name>
pkill gunicorn
```

- docker-compose
```
sudo docker-compose build
# 查看當前的鏡像
sudo docker images
# 背景執行docker-compose
sudo docker-compose up -d
# 重新build docker-compose後，背景執行docker-compose
sudo docker-compose up -d --build
# 關閉docker-compose
docker-compose down
# 查看運行中的容器
sudo docker ps
# 移除none images
docker rmi $(docker images -f "dangling=true" -q)
```

### 部屬到Heroku
- 在部屬環境中，請自行增加`.env`檔案
```
SECRET_KEY=xxx
DJANGO_SETTINGS_MODULE=Maple.settings.heroku
DEBUG=False
DATABASE_HOST=xxx.com
DATABASE_NAME=xxx
DATABASE_USER=xxx
DATABASE_PORT=5432
DATABASE_PASSWORD=xxx
DATABASE_URI=postgres://xxx
```

- 把.env檔新增到heroku config內
```
heroku config:set $(cat .env | sed '/^$/d; /#[[:print:]]*$/d')
```

- 部屬Heroku流程
    1. 增加Procfile
        ```
        web: gunicorn Maple.wsgi --log-file -
        release: python manage.py migrate
        ```
    2. 指定heroku上面python的版本(runtime.txt)
        ```
        python-3.7.12
        ```
    3. 確保當前套件都有引入
        ```
        pip freeze > requirements.txt
        ```
    4. 部屬到heroku上面
        ```
        - git init
        - git add .
        - git commit -m "init project"
        - heroku login
        - heroku config:set $(cat .env | sed '/^$/d; /#[[:print:]]*$/d')
        - heroku config
        - git push heroku `your-branch`:master
        - heroku run python manage.py createsuperuser
        ```
    5. Debug
        ```
        - heroku pg
        - heroku logs -t
        - heroku logs --dyno sched
        - heroku logs --source app --dyno worker
        - heroku run python manage.py shell
        ```
    6. 其他語法
        ```
        - heroku releases
        - heroku addons
        - heroku maintenance:on
        - heroku local -f Procfile.windows
        - heroku run python manage.py shell
        - heroku run python manage.py migrate
        - heroku run bash -a <app_name>
        ```

### 部屬到GCP(GKE)
- [教學](https://medium.com/peerone-technology-%E7%9A%AE%E5%81%B6%E7%8E%A9%E4%BA%92%E5%8B%95%E7%A7%91%E6%8A%80/%E6%89%8B%E6%8A%8A%E6%89%8B%E5%B0%87-django-%E6%9C%8D%E5%8B%99%E9%80%81%E4%B8%8A-gcp-6a29ca30a6f)
- [CORS問題](https://hoohoo.top/blog/resolving-gcp-storage-to-get-data-to-occur-blocked-by-cors-policy/)

### 部屬到Fly io(docker images)
- [官方教學](https://fly.io/docs/languages-and-frameworks/dockerfile/)
- [教學](https://fly.io/docs/languages-and-frameworks/dockerfile/)

1. 下載fly io
2. 配置新的fly.toml、Dockerfile。這邊需要選擇DB規格
    ```
    fly launch
    ```
3. 進行部屬
    ```
    fly deploy
    ```
4. 遇到的問題
    1. DB無法進入新增的專案
        ```
        fly postgres attach --app mapleweb2 mapleweb2-db  # 再次進行專案與DB間的附加 來找錯誤
        fly doctor  # 用來找bug
        flyctl wireguard reset  # 嘗試重新設定wireguard
        iptables -A INPUT -p udp --dport 51820 -j ACCEPT   # 允許某個port進行訪問
        ```
5. 其他語法
    ```
    fly ssh console -C 'ls -l /app'
    fly ssh console -C 'python /app/manage.py shell'
    fly ssh console -C 'python /app/manage.py migrate'
    fly secrets list  # 取得所有環境變數
    fly secrets set REDIS_PASSWORD=mypassword
    fly secrets set DJANGO_SETTINGS_MODULE=Maple.settings.fly  # 設定環境變數
    fly secrets unset DJANGO_SETTINGS_MODULE  # 移除某個環境變數
    ```

#### 增加redis配置
1. 在對應的apps底下創建新的redis服務
    ```shell script
    flyctl redis create
    ```
2. 創建之後會給fly上面的redis url就能進行連線了
    ```python
   import redis
   url = ""
   r = redis.from_url(url)
   r.ping()  # If true, the connection is successful.
    ```
    

#### CD deploy到fly.io
- [官方教學](https://fly.io/docs/app-guides/continuous-deployment-with-github-actions/)
- 主要就照貼就行了
```
  deploy:
    name: Deploy Django
    needs: tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### 效能測試
- 相同的查詢條件下，比較各種部屬方式(Postman)
- `{server_url}/exchange/product-list?category=武器&type=雙手劍&stage_level=普通`

| server_url | 平均執行時間 | 備註 |
| :--------- | :---------- | ---- |
| 127.0.0.1:8000 | 22ms | local端連接VM端DB |
| 192.168.223.127:8080 | 24ms | VM端連接VM端DB |
| ngrok | 800ms | ngrok https + VM端連接VM端DB |
| 127.0.0.1:5000 | 3.69s | heroku端連接heroku端DB |

### 第三方登入(前後端分離)
- Google
    - [教學文章](https://blog.hanklu.tw/post/2020/spa-api-social-loign/)

### 撰寫方式
- 寫在view.py內
    - 欄位判斷(是否存在、是否有共存關係)
    - 是否是對應的使用者
- 寫在serializer.py內
    - CRUD的實際操作邏輯(某些欄位不進行更新)
    - 修改真正要顯示的欄位內容

### 其他
- Makefile
```
建議搭配著linux中的zsh-autoswitch_virtualenv使用
mkvenv --python=$(which python3.7) --把該專案設定成指定的python版本
```

- 增加gitignore
```
curl https://www.toptal.com/developers/gitignore/api/python,pycharm+all,django > .gitignore
```

- Heroku上面串接google storage
```
[教學文章](https://kavenc.gitlab.io/blog/post/django-google-cloud-storage/#gsc.tab=0)
```

### Todo
- [ ] 修改ProductList、Product儲存images的格式 images => blob
    - [blob](https://stackoverflow.com/questions/66470537/how-do-i-save-images-directly-into-a-mysql-database-as-a-blob-using-django-thes)

1. user 增加phone、sms_code、game_name、game_image(遊戲截圖[sms_code + game_name])、is_valid(遊戲截圖驗證)
   - 人工驗證 => 自動驗證機制(todo)
       - 驗證圖片上的sms_code、game_name 是否吻合
   - 通過驗證者，有藍勾勾(is_vaild)
   - 跟用戶提倡買賣前，請先確認對方角色名稱是否與平台吻合，在進行交易
2. 嘗試看看ProductListForm type不必填 測測看速度
    - python manage.py shell_plus --print-sql
- [X] 上架商品增加 (超越、製作)失敗次數


### 引用套件
- [django-simple-UI](https://simpleui.72wo.com/docs/simpleui/doc.html#%E4%BB%8B%E7%BB%8D)
- [django-simple-history](https://django-simple-history.readthedocs.io/en/latest/)
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)
- [django-gcloud-storage](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html)
- [apscheduler](https://apscheduler.readthedocs.io/en/3.x/index.html)
