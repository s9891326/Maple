web: gunicorn Maple.wsgi --max-requests 1200 --log-level debug
sched: python worker/sched.py
release: python manage.py migrate