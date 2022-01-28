FROM python:3.7

MAINTAINER Eddy

# 環境變數 (這行是告訴 python，有 log 就往外吐)
# 可參考 Is PYTHONUNBUFFERED=TRUE a good idea?
# (https://github.com/awslabs/amazon-sagemaker-examples/issues/319)
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/www/html/django_deploy

# 在容器内/var/www/html/下创建 django_deploy文件夹
RUN mkdir -p /var/www/html/django_deploy

WORKDIR /var/www/html/django_deploy

ADD . /var/www/html/django_deploy

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

# Windows环境下编写的start.sh每行命令结尾有多余的\r字符，需移除。
RUN sed -i 's/\r//' ./start.sh

RUN chmod +x ./start.sh
