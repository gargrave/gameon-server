from .base import *

DEBUG = True
BUILD = 'dev'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gameon_dev',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 500
    }
}

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    'localhost:8080',
)

# for dev builds, read the secret key from file
with open('etc/dev_secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
