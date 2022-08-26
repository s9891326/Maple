web: gunicorn Maple.wsgi --timeout 1200 --log-level debug
sched: python worker/sched.py
release: python manage.py migrate