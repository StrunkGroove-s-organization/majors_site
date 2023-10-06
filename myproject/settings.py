import os

from pathlib import Path

from .secrets import (
    DEFAULT_PG_NAME, DEFAULT_PG_USER, DEFAULT_PG_PASSWORD, 
    DEFAULT_PG_HOST, DEFAULT_PG_PORT
)

from .secrets import (
    DEFAULT_REDIS_HOST, DEFAULT_REDIS_PORT, DEFAULT_REDIS_NUMBER
)

from .secrets import (
    WITHOUT_REDIS_PASSWORD, WITHOUT_REDIS_HOST, 
    WITHOUT_REDIS_PORT, WITHOUT_REDIS_NUMBER
)

from .secrets import (
    P2P_REDIS_PASSWORD, P2P_REDIS_HOST, P2P_REDIS_PORT, P2P_REDIS_NUMBER
)

from .secrets import (
    EMAIL_BACKEND, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
)

from .secrets import SECRET_KEY


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ['arbitools.ru']

INSTALLED_APPS = [
    'main',
    'price',
    'p2plinks',
    'accounts',
    'user_profile',
    'blog',
    'cookies',
    'block_spreadtable',
    'payment',
    'register',
    'links_without_cards',

    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DEFAULT_PG_NAME,
        'USER': DEFAULT_PG_USER,
        'PASSWORD': DEFAULT_PG_PASSWORD,
        'HOST': DEFAULT_PG_HOST,
        'PORT': DEFAULT_PG_PORT
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": (
            f'redis://{DEFAULT_REDIS_HOST}'
            f':{DEFAULT_REDIS_PORT}/{DEFAULT_REDIS_NUMBER}'
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "links_without_cards": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": (
            f'redis://:{WITHOUT_REDIS_PASSWORD}@{WITHOUT_REDIS_HOST}'
            f':{WITHOUT_REDIS_PORT}/{WITHOUT_REDIS_NUMBER}'
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "p2p_server": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": (
            f'redis://:{P2P_REDIS_PASSWORD}@{P2P_REDIS_HOST}'
            f':{P2P_REDIS_PORT}/{P2P_REDIS_NUMBER}'
        ),
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

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

### LOGGING configuration ###

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logfile.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
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
        'anon': '20/minute',
        'user': '20/minute',
    }
}

### REDIS configuration ###

CELERY_BROKER_URL = (
    f'redis://{DEFAULT_REDIS_HOST}:{DEFAULT_REDIS_PORT}/{DEFAULT_REDIS_NUMBER}'
)
CELERY_RESULT_BACKEND = (
    f'redis://{DEFAULT_REDIS_HOST}:{DEFAULT_REDIS_PORT}/{DEFAULT_REDIS_NUMBER}'
)
CELERY_TIMEZONE = 'UTC'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASKSERILIZER =  'json'
