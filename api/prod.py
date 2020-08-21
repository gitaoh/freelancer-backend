"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from datetime import timedelta

from rest_framework.settings import api_settings

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [str(os.environ.get('BackendAppUrl'))]

CORS_ORIGIN_WHITELIST = (os.environ.get('FrontEndUrl'),)

ADMINS = [(os.environ.get('ADMIN_ONE'), os.environ.get('ADMIN_ONE_EMAIL')),
          (os.environ.get('ADMIN_TWO'), os.environ.get('ADMIN_TWO_EMAIL'))]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': str(os.environ.get('DATABASE_DB')),
        'NAME': str(os.environ.get('DATABASE_NAME')),
        'HOST': str(os.environ.get('DATABASE_HOST')),
        'USER': str(os.environ.get('DATABASE_USER')),
        'PORT': str(os.environ.get('DATABASE_PORT')),
        'PASSWORD': str(os.environ.get('DATABASE_PASSWORD')),
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

REST_KNOX = {
    'AUTH_TOKEN_CHARACTER_LENGTH': 128,
    'TOKEN_TTL': timedelta(days=3),
    'TOKEN_LIMIT_PER_USER': 10,
    'AUTO_REFRESH': True,
    'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}

# Email configurations
EMAIL_HOST = os.environ.get('EMAIL_HOST')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# The optional username to use to authenticate to the SMTP server.
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')

# The optional password to use to authenticate to the SMTP server
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_USER')
