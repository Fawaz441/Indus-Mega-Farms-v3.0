# import os
# from mode import dev
# from django.conf import settings
# from celery.schedules import crontab
# from celery import Celery

# # set the default Django settings module for the 'celery' program.
# if dev:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'indus_mega_farms.settings.dev')
# else:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'indus_mega_farms.settings.prod')

# app = Celery('indus_mega_farms')

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.update(
#     task_serializer='json',
#     accept_content=['json'],  # Ignore other content
#     result_serializer='json',
#     timezone='Africa/Lagos',
#     enable_utc=True,
# )



# if not dev:
#     app.conf.update(broker_url=os.environ['REDIS_URL'], result_backend=os.environ['REDIS_URL'])
# else:
#     # app.conf.update(broker_url=DEV_REDIS_URL, result_backend=DEV_REDIS_URL)
#     pass

# app.conf.beat_schedule = {
#      'delete-expired-ads': {
#          'task': 'delete_expired_ads',
#          'schedule': crontab(minute=0, hour=0),
#      }
# }


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
    
# # celery -A drat beat
# # celery -A drat worker --loglevel=INFO
# # 