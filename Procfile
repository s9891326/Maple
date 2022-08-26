web: gunicorn Maple.wsgi --log-file -
web: gunicorn Maple.wsgi --max-requests 1200
sched: python worker/sched.py
release: python manage.py migrate