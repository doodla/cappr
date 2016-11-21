from .base import *

DEBUG = True

INSTALLED_APPS += [
]

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

API_KEY_VISION = '4c285f0cf6df46ce923e0514dd2361b0'
URL_VISION_API = 'https://api.projectoxford.ai/vision/v1.0/analyze'
NUM_OF_RESULTS = 50
