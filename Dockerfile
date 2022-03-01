FROM python:3.7

MAINTAINER Eddy

# 環境變數 (這行是告訴 python，有 log 就往外吐)
# 可參考 Is PYTHONUNBUFFERED=TRUE a good idea?
# (https://github.com/awslabs/amazon-sagemaker-examples/issues/319)
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/Maple

# 在容器内/var/www/html/下创建 maple_web文件夹
RUN mkdir -p /var/Maple

WORKDIR /var/Maple

ADD . /var/Maple

RUN apt-get update && apt-get install -y \
    gettext \
    vim

EXPOSE 8000

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .
