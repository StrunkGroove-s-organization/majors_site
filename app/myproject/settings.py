import os
from os import getenv
from pathlib import Path

SECRET_KEY = getenv('SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = getenv('ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = getenv('CSRF_TRUSTED_ORIGINS').split(',')
CSRF_ALLOWED_ORIGINS = getenv('CSRF_ALLOWED_ORIGINS').split(',')
CORS_ORIGINS_WHITELIST = getenv('CORS_ORIGINS_WHITELIST').split(',')


EXTENSIONS_APP = [
    'main',
    'price',
    'p2plinks',
    'accounts',
    'user_profile',
    'blog',
    'payment',
    'register',
    'refferal',
    'links_without_cards',

    'rest_framework',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + EXTENSIONS_APP

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'refferal.middleware.ReferralMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'myproject.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('POSTGRES_DB'),
        'USER': getenv('POSTGRES_USER'),
        'PASSWORD': getenv('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': getenv('POSTGRES_PORT'),
    },
    'links_without_cards': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('WITHOUT_PG_NAME'),
        'USER': getenv('WITHOUT_PG_USER'),
        'PASSWORD': getenv('WITHOUT_PG_PASSWORD'),
        'HOST': getenv('WITHOUT_PG_HOST'),
        'PORT': getenv('WITHOUT_PG_PORT'),
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 
            f"redis://redis:{getenv('DEFAULT_REDIS_PORT')}/ \
            {getenv('DEFAULT_REDIS_NUMBER')}",

        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "p2p_server": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 
            f"redis://:{getenv('P2P_REDIS_PASSWORD')}@ \
            {getenv('P2P_REDIS_HOST')}: \
            {getenv('P2P_REDIS_PORT')}/ \
            {getenv('P2P_REDIS_NUMBER')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

### Password validation ###

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

### Internationalization ###

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

### USER MODEL ###

AUTH_USER_MODEL = 'accounts.User'

### STATIC FILE configuration ###

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

### LOGGING configuration ###

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logfile.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

### REST FRAMEWORK configuration ###

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute',
        'user': '60/minute',
    }
}

### REDIS configuration ###

CELERY_BROKER_URL = f"redis://redis:{getenv('DEFAULT_REDIS_PORT')}/{getenv('DEFAULT_REDIS_NUMBER')}"
CELERY_RESULT_BACKEND = f"redis://redis:{getenv('DEFAULT_REDIS_PORT')}/{getenv('DEFAULT_REDIS_NUMBER')}"
CELERY_TIMEZONE = 'UTC'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASKSERILIZER =  'json'

### Email ###

EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_PORT = getenv('EMAIL_PORT')
EMAIL_USE_TLS = getenv('EMAIL_USE_TLS').upper() == 'TRUE'
EMAIL_BACKEND = getenv('EMAIL_BACKEND')
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')

