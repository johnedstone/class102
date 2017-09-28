import os
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
     hashlib.sha1(os.urandom(128)).hexdigest(), 
)
DEBUG = os.environ.get('DEBUG', 'on') == 'on'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost 127.0.0.1').split()
INTERNAL_IPS = os.environ.get('INTERNAL_IPS', 'localhost 127.0.0.1').split() 


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'debug_toolbar',
    'bootstrapform',

    # apps
    'chap3_app',

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
]

ENABLE_WHITENOISE = os.environ.get('ENABLE_WHITENOISE', 'off') == 'on' # Added for origin/openshift
if ENABLE_WHITENOISE:
    MIDDLEWARE_CLASSES.append('whitenoise.middleware.WhiteNoiseMiddleware')

MIDDLEWARE_CLASSES += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'chap3_project.urls'

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

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
  project_logging_level = 'INFO'
else:
  project_logging_level = 'WARNING'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s:%(module)s:%(lineno)d:%(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': project_logging_level,
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'verbose_logging': {
            'handlers': ['console',],
            'level': project_logging_level,
            'filters': ['require_debug_true']
        }
    }
}

# v0.4
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/servers/private/'

# v0.5

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

USE_TERMINATION_EDGE = os.environ.get('USE_TEMINATION_EDGE', 'off') == 'on'
if USE_TERMINATION_EDGE:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# vim: ai et ts=4 sts=4 sw=4 ru nu
