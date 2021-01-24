import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")
MEDIA_ROOT = os.path.join(BASE_DIR,"media")

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
    'ads',
    'crispy_forms',
    'pinax.referrals',
    'account',
    'storages',
    'paystack',
    'django_inlinecss',
    'i_competitions',
    'blog',
    'django_summernote'
]

# for django summernote
X_FRAME_OPTIONS = 'SAMEORIGIN'


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

SITE_ID = 1
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# PINAX_REFERRALS_SECURE_URLS = False

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


LOGIN_REDIRECT_URL = 'users:user_home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'users:login'

ACCOUNT_EMAIL_CONFIRMATION_EMAIL = False
ACCOUNT_SIGNUP_REDIRECT_URL = 'users:category'



PAYSTACK_SUCCESS_URL = 'users:user_home'
PAYSTACK_FAILURE_URL = 'products:order_final'

# AWS
AWS_ACCESS_KEY_ID = os.getenv('AWS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

STATIC_ROOT = os.path.join(BASE_DIR,"staticfiles")
STATICFILES_DIRS = (
	os.path.join(BASE_DIR,'static'),
)

# s3 stuff
