from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ENVIRONMENT['pg_database'],
        'USER': ENVIRONMENT['pg_user'],
        'PASSWORD': ENVIRONMENT['pg_password'],
        'HOST': ENVIRONMENT['pg_host'],
        'PORT': ENVIRONMENT['pg_port'],
    }
}