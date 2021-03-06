"""
Django settings for prez_party project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url
# from talk_app.custom_storages import StaticStorage

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'amc7c=vt*a6oz5(p#%-6f27@k0amm_2716v-w*l#=lvi#aax85'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'talk_app',
    'social.apps.django_app.default',  # python social auth
    'storages',  # s3

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',  # python social auth
]

ROOT_URLCONF = 'prez_party.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',  # python social auth
                'social.apps.django_app.context_processors.login_redirect',  # python social auth

            ],
        },
    },
]

WSGI_APPLICATION = 'prez_party.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# FROM HERE python social auth
AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
    )
SOCIAL_AUTH_TWITTER_KEY = os.getenv("tw_consumer_key")
SOCIAL_AUTH_TWITTER_SECRET = os.getenv("tw_consumer_secret")

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/party/view/'
SOCIAL_AUTH_LOGIN_URL = '/party/view/'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username']
SOCIAL_AUTH_URL_NAMESPACE = 'social'
# TO HERE python social auth

# FROM HERE storage on AWS
# get all the secret stuff from hidden file
aws_bucket_name = os.environ.get('aws_bucket_name')

AWS_STORAGE_BUCKET_NAME = aws_bucket_name
AWS_ACCESS_KEY_ID = os.getenv('aws_key')
AWS_SECRET_ACCESS_KEY = os.getenv('aws_secret')

AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(aws_bucket_name)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_URL = '/static/'

if aws_bucket_name:
    AWS_S3_FILE_OVERWRITE = False
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    # STATIC_URL = "https://{}/".format(AWS_S3_CUSTOM_DOMAIN)
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles') # errors on  ?????????
# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  ??????????
# STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)  ??????????
STATIC_ROOT = BASE_DIR + "/static"
STATICFILES_LOCATION = 'static'

# TO HERE storage on AWS

# STATICFILES_STORAGE = 'custom_storages.StaticStorage'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR

USE_THOUSAND_SEPARATOR = True
