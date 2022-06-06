web: gunicorn Maple.wsgi --log-file -
sched: python worker/sched.py
release: python manage.py migrate