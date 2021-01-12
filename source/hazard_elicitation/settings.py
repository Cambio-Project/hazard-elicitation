import os
from util.config import Config
from util.path import path

ALLOWED_HOSTS = ['*']
BASE_DIR = path(__file__, '..', '..')
CONFIG = Config(path(BASE_DIR, '..', 'config.json'))
CSRF_COOKIE_SECURE = True
DEBUG = False
FORMATTED_LOGGING = True
KEYS = Config(path(BASE_DIR, '..', 'keys.json'))
LANGUAGE_CODE = 'en-us'
ROOT_URLCONF = 'hazard_elicitation.urls'
SECRET_KEY = KEYS.get('django_secret')
SESSION_COOKIE_SECURE = True
STATIC_ROOT = '.' if DEBUG else path(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [path(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
VERSION = '0.5.0'

ASGI_APPLICATION = 'hazard_elicitation.asgi.application'
WSGI_APPLICATION = 'hazard_elicitation.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   str(path(BASE_DIR, 'db.sqlite3')),
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'channels',

    'architecture_extraction_backend',
    'dialogflow_backend'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND':  'django.template.backends.django.DjangoTemplates',
        'DIRS':     [
            os.path.join(BASE_DIR, 'static')
        ],
        'APP_DIRS': True,
        'OPTIONS':  {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
