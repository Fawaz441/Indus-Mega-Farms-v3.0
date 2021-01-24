release: python manage.py migrate
web: gunicorn indus_mega_farms.wsgi.prod --log-file -
worker: celery -A indus_mega_farms worker -B --loglevel=INFO