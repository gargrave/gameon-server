import os
import dj_database_url

from .base import *

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = True
BUILD = 'staging'

DATABASES = {'default': dj_database_url.config()}
# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

CORS_ORIGIN_WHITELIST = (
    'https://PLACEHOLDER_URL.com',
    'PLACEHOLDER_URL.com',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
