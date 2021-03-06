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

ALLOWED_HOSTS = []
SECRET_KEY = 'C2LUQecD4QKoDz-0XtbRJ1m5n_uPmE7OGWurK4BLA4Q'

# Application definition

CORS_ORIGIN_WHITELIST = ("http://127.0.0.1:3000",)

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'api',
        'HOST': '127.0.0.1',
        'USER': 'postgres',
        'PORT': '5432',
        'PASSWORD': '50391798',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'example@gmail.com'
EMAIL_HOST = "smtp.mailtrap.io"
EMAIL_PORT = "465"
EMAIL_HOST_USER = "04395d2e790d4d"
EMAIL_HOST_PASSWORD = "6ac9ea9db1be70"
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True

REST_KNOX = {
    'AUTH_TOKEN_CHARACTER_LENGTH': 128,
    'TOKEN_TTL': timedelta(days=3),
    'TOKEN_LIMIT_PER_USER': 10,
    'AUTO_REFRESH': True,
    'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}
