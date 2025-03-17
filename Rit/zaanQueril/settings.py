"""
Django settings for zaanQueril project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
# from celery.schedules import crontab
from pathlib import Path
import os
from datetime import timedelta
# from celery.schedules import crontab
# import time

# system_timezone = time.tzname
# print("System's timezone:", system_timezone)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jiuvi6i52@^b*%su12v9(rk4yle&jaeeca8ho57063bbz(xo&j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['www.ritcoin.exchange','ritcoin.exchange','159.253.60.37']
# ALLOWED_HOSTS = ['103.209.146.152','rimberio.world','www.rimberio.world']

CSRF_FAILURE_VIEW = 'zqapp.views.custom_csrf_failure_view'

# Application definition

INSTALLED_APPS = [
    # 'channels' , 
    # "daphne",
    'django_celery_beat',
    # 'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'zqUsers',
    'anymail',
    # 'apitest',
    'zqapp',
    'wallet',
    'zqAdmin',

       
]



MIDDLEWARE = [
    # 'zqUsers.maintenance_middleware.MaintenanceMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #  'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'zaanQueril.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
           
                # 'zqAdmin.context_processors.getZQLRate',
                'zqUsers.context_processors.getZQLRate',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ASGI_APPLICATION = 'zaanQueril.asgi.application'

# WSGI_APPLICATION = 'zaanQueril.wsgi.application'
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

DATABASES = {
    
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ritcoinexchange',
        # 'NAME': 'pocketmoneytesting',
        'USER': '',
        'HOST': 'localhost',
        'PASSWORD':'',
        'PORT': 3306,
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
            
        },
        'TIME_ZONE': 'Asia/Kolkata',
    }
 

}

AUTHENTICATION_BACKENDS = [
    
       
    'zqUsers.backends.ZqUserEmailBackend',
    'django.contrib.auth.backends.ModelBackend',  # Keep ModelBackend for other authentication methods
]


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/



LANGUAGE_CODE = 'en-us'
USE_TZ = True
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
# USE_TZ = True




STATIC_URL = '/static/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# print(BASE_DIR)
STATICFILES_DIRS=[
                 os.path.join(BASE_DIR / 'static'),
              
                ]



AUTH_USER_MODEL = 'zqUsers.ZqUser'
# ===========================================

EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_USE_TLS = False
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''


ANYMAIL = {
    "SENDINBLUE_API_KEY": 'asvdsssvsvsvsvsvsv',

    "SEND_DEFAULTS": {
        "tags": ["app"]
    },
    "DEBUG_API_REQUESTS": DEBUG,
}

# SESSION_COOKIE_AGE = 600  # Set session expiry to 1 hour (3600 seconds)


# SESSION_COOKIE_AGE = None

# STATIC_ROOT=os.path.join(BASE_DIR,"static")

STATIC_ROOT = BASE_DIR / "staticfiles"
# STATIC_ROOT = BASE_DIR / "static"


# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'


# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# # CELERY_TIMEZONE = 'UTC'
# CELERY_TIMEZONE = 'Asia/Kolkata'




MEDIA_ROOT = '/home/ritcoin/media/media/uploadedDocuments/'

# CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'  
# e.g., 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'disabled://'

# CELERY_TIMEZONE = 'UTC'
# TIME_ZONE = 'Asia/Kolkata'

# CELERY_TIMEZONE = 'UTC'

# CELERY_BEAT_SCHEDULE = {
#     'task-name': {
#         'task': 'zqUsers.tasks.distributeReturn',
#         'schedule': 86400,  # Schedule the task to run every 60 seconds
#         # 'args': (3, 5),  # Schedule the task to run every 60 seconds
#     },
    
#     # 'task_at_midnight': {
#     #     'task': 'zqUsers.tasks.pppp',  # Task to execute
#     #     'schedule': crontab(hour=12, minute=14),  # Schedule task to run at 12:00 AM (midnight) every day
#     # },
# }

# print(crontab(hour=0, minute=56))

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': '/home/pocketmoney/survapp/staticfiles/shifraErrors.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# print("==================================")
print(MEDIA_ROOT)
# print("==================================")
# LOGOUT_REDIRECT_URL = '/'