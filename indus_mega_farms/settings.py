import django_heroku
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")
MEDIA_ROOT = os.path.join(BASE_DIR,"media")

ALLOWED_HOSTS = ['www.indusmegafarms.com','localhost','127.0.0.1']



SECRET_KEY = os.getenv('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'products',
    'users',
    'crispy_forms',
    'pinax.referrals',
    'account',
    'storages',
    'paystack',
    'i_competitions',
    'ads'
]

SITE_ID = 1
CRISPY_TEMPLATE_PACK = 'bootstrap4'


PINAX_REFERRALS_SECURE_URLS = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True



MIDDLEWARE = [
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'pinax.referrals.middleware.SessionJumpingMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = 'indus_mega_farms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'indus_mega_farms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {}
import dj_database_url 
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# AWS
AWS_ACCESS_KEY_ID = os.getenv('AWS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR,"staticfiles")
STATICFILES_DIRS = (
	os.path.join(BASE_DIR,'static'),
)

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
PAYSTACK_SUCCESS_URL = 'users:user_home'
PAYSTACK_FAILURE_URL = 'products:order_final'
PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC')
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET')

# EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'indusmegafarms@gmail.com'
EMAIL_HOST_PASSWORD = 'zewmjrpkllyrzwws'

django_heroku.settings(locals(),staticfiles=False)
# del DATABASES['default']['OPTIONS']['sslmode']



LOGIN_REDIRECT_URL = 'users:user_home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'users:login'

ACCOUNT_EMAIL_CONFIRMATION_EMAIL = False
ACCOUNT_SIGNUP_REDIRECT_URL = 'users:category'

