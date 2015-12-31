from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'foodinspector',
        'USER': 'foodinspector',
        'PASSWORD': 'foodman',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}