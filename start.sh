#!/bin/bash

python manage.py collectstatic --noinput&&
python manage.py makemigrations&&
python manage.py migrate&&
uwsgi --ini /var/maple_web/uwsgi.ini