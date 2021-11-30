import os
import datetime

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '6-ov!s%*3os)xu(77s@-45#@)v1otz2w4+r@1tlh&o*t52q1i!'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',

    'corsheaders',
    'drf_yasg',

    'users.apps.UsersConfig',
    'constructor.apps.ConstructorConfig',
    'versatileimagefield',

]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'src.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }


AUTH_USER_MODEL = 'users.UserAccount'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = (
    str(BASE_DIR / 'static_dev'),
)

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',
        'user': 'users.serializers.UserCreateSerializer',
        'current_user': 'users.serializers.UserCreateSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    }
}
# signals tg
TG_BROKER_URL = 'http://localhost:6000'

# CORS WHITELIST
# CORS_ORIGIN_ORIGINS = [
#     "http://localhost:8080",
#     "http://localhost:8081",
#     "http://127.0.0.1:8000",
#     'http://85.214.76.64',
#     'http://www.calendarbot.net'
#
# ]
# CORS WHITELIST
CORS_ALLOW_ALL_ORIGINS = True
# # CORS_ALLOWED_ORIGINS = [
# #     "http://localhost:8080",
# #     "http://localhost:8000",
# #     "http://localhost:7000",
# #     'localhost',
# #     "http://localhost",
# # ]

# CORS_ORIGIN_REGEX_WHITELIST = [
#     r"^http://\w+\.botconstrucctor\.ru$",
#     r"^http://$",
# ]
"""настройки бота"""
# Ставим вебхук
# api.telegram.org/bot997719198:AAEi_fXpSJEhni6Lpsc5O1Q7abl5sBE7JXc/setwebhook?url=https://d7687b0d39c0.ngrok.io
# http://api.telegram.org/bot1577812306:AAESS6a5ge3-sDkaKSz8VgJz2g_I8LeTzSE/setwebhook?url=https://9e5a3dfab31f.ngrok.io

# Проверяем бота
# curl https://api.telegram.org/bot1577812306:AAESS6a5ge3-sDkaKSz8VgJz2g_I8LeTzSE/getWebhookInfo
# TOKEN = '1577812306:AAESS6a5ge3-sDkaKSz8VgJz2g_I8LeTzSE'
