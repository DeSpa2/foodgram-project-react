import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-((8+v817(gi36yi&6o-+mrvdr298$a3$f4@fa*!s!r+m7d01$1'

DEBUG = False

ALLOWED_HOSTS = [
    '51.250.100.110',
    'yaproject.ddns.net',
    'localhost',
    'backend',
    '*'
]

INSTALLED_APPS = [
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.getenv(
            "DB_ENGINE", default="django.db.backends.postgresql"
        ),
        "NAME": os.getenv("DB_NAME", default="postgres"),
        "USER": os.getenv("POSTGRES_USER", default="postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="postgres"),
        "HOST": os.getenv("DB_HOST", default="db"),
        "PORT": os.getenv("DB_PORT", default="5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/admin/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/admin")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "HIDE_USERS": False,
    "PERMISSIONS": {
        "user": ("api.permissions.OwnerOrReadOnly",),
        "user_list": ("api.permissions.OwnerOrReadOnly",),
    },
    "SERIALIZERS": {
        "user": "api.serializers.UserSerializer",
        "user_list": "api.serializers.UserSerializer",
        "current_user": "api.serializers.UserSerializer",
        "user_create": "api.serializers.UserSerializer",
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG" if DEBUG else "ERROR",
            "handlers": [
                "console",
            ],
        },
    },
}

MAX_LEGTH = 100
MAX_LEN_RECIPES = 1000
MAX_EMAIL_LENGTH = 255
MAX_USERNAME_LENGTH = 150
MAX_PASSWORD_LENGTH = 150
MIN_COOK_TIME = 1
MAX_COOK_TIME = 300
MIN_AMOUNT_INGREDIENTS = 1
MAX_AMOUNT_INGREDIENTS = 100
PAGE_SIZE = 8
RECIPE_IMAGE_SIZE = 500, 300
ADD_METHODS = "GET", "POST"
DEL_METHODS = "DELETE"
ACTION_METHODS = "GET", "POST", "DELETE"
SYMBOL_TRUE_SEARCH = "1", "true"
SYMBOL_FALSE_SEARCH = "0", "false"
EXTRA = 1

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATE_TIME_FORMAT = "%d/%m/%Y %H:%M"