from .base import *

SECRET_KEY = "BitCamp-სწავლა-და-ბრძოლა-1024"

DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

# Database

# Replace this values according to your development database
DATABASES = {
   "default": {
       "ENGINE": "django.db.backends.postgresql",
       "NAME": "bitbase",
       "USER": "postgres",
       "PASSWORD": "bitpass",
       "HOST": "localhost",
       "PORT": "5432",
   }
}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"
}

SPECTACULAR_SETTINGS = {
    "TITLE": "BitCamp backend"
}