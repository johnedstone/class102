import hashlib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY',
                             hashlib.sha1(os.urandom(128)).hexdigest(),)

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost 127.0.0.1').split()

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # Internal apps
    'aws_bucket_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restapi_project.urls'

#TEMPLATES = [
#    {
#        'BACKEND': 'django.template.backends.django.DjangoTemplates',
#        'DIRS': [os.path.join(BASE_DIR, 'templates')],
#        'APP_DIRS': True,
#        'OPTIONS': {
#            'context_processors': [
#                'django.template.context_processors.debug',
#                'django.template.context_processors.request',
#                'django.contrib.auth.context_processors.auth',
#            ],
#        },
#    },
#]

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
               'rest_framework.renderers.JSONRenderer',)

# For using SSL with openshift
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# For v0.8
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', 'hocospocus')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', 'hocospocus')

# For v0.9
HTTP_PROXY = os.getenv('HTTP_PROXY')
HTTPS_PROXY = os.getenv('HTTPS_PROXY')
# vi: ai et ts=4 sts=4 sw=4 nu ru
