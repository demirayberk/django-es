import os
from pathlib import Path
from typing import Any, Dict, List, TypedDict

from dotenv import load_dotenv

load_dotenv()


class Template(TypedDict):
    BACKEND: str
    DIRS: List[Any]
    APP_DIRS: bool
    OPTIONS: Dict[str, List[str]]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

SECRET_KEY = os.getenv("SECRET_KEY", "")
DEBUG = os.getenv("DEBUG", "")

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "api",
    "drf_yasg",
    'django_celery_beat',
    'django_celery_results',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.auth.CustomTokenAuthentication",  # Add your custom authentication class
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # This is correct
    ],
}

AUTH_SIGNATURE = os.getenv("AUTH_SIGNATURE", "")
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "CustomTokenAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": f"Custom token authentication. Prefix your token with {AUTH_SIGNATURE}. Example: {AUTH_SIGNATURE} <your_token>",
        },
    },
    "USE_SESSION_AUTH": False,
}

ROOT_URLCONF = "core.urls"

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "")

CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

TEMPLATES: List[Template] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("NAME", ""),
        "USER": os.getenv("USER", ""),
        "PASSWORD": os.getenv("PASSWORD", ""),
        "HOST": os.getenv("HOST", ""),
        "PORT": os.getenv("PORT", ""),
    }
}

ES_HOST = os.getenv("ES_HOST", "")
ES_INDEX = os.getenv("ES_INDEX", "")


MOCK_USERNAME = os.getenv("MOCK_USERNAME", "")
MOCK_PASSWORD = os.getenv("MOCK_PASSWORD", "")
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# CELERY_BEAT_SCHEDULE = {
#     'run-every-10-seconds': {
#         'task': 'api.tasks.mock_task',
#         'schedule': 10.0,  # Run every 10 seconds
#     },
# }

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



STATIC_URL = "static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
