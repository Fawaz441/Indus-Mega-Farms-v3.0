from .base import *

import django_heroku
import os

ALLOWED_HOSTS = ['www.indusmegafarms.com']

SECRET_KEY = os.getenv('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

WSGI_APPLICATION = 'indus_mega_farms.wsgi.prod.application'



# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {}
import dj_database_url 
DATABASES['default'] = dj_database_url.config(conn_max_age=600)




DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_MEDIA_DOMAIN = 'indusmegabucket.s3.amazonaws.com/media/'

MEDIA_URL = AWS_S3_MEDIA_DOMAIN

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
STATIC_URL = 'https://%s/' % (AWS_S3_CUSTOM_DOMAIN)

# PAYSTACK

PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC')
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET')

# EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')

django_heroku.settings(locals(),staticfiles=False)
# del DATABASES['default']['OPTIONS']['sslmode']

