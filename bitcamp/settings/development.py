from .base import *

SECRET_KEY = "BitCamp-სწავლა-და-ბრძოლა-1024"

DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"
}

SPECTACULAR_SETTINGS = {
    "TITLE": "BitCamp backend"
}