
from .base import *
import os

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'vv1-$^5scde1=%b!sj^84_0tnfi9dgs7+nc$9m9a+x%hzc%+qr'
DEBUG = True
# Application definition


WSGI_APPLICATION = 'indus_mega_farms.wsgi.dev.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



STATIC_ROOT = os.path.join(BASE_DIR,"staticfiles")
STATICFILES_DIRS = (
	os.path.join(BASE_DIR,'static'),
)


MEDIA_URL = '/media/'


STATIC_URL = '/static/'


PAYSTACK_PUBLIC_KEY = 'pk_test_e597d08defcddc00c7286af4abdefc2aa8c04fda'
PAYSTACK_SECRET_KEY = 'sk_test_26b451928ea2a8504b37d2caffe2a2d60bc64a2b'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
