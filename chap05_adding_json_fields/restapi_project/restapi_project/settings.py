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

    # enabled for swagger
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',

    # Not needed as no UI is using this rest api
    # 'corsheaders',

    # Internal apps
    'aws_bucket_app',
    'rest_framework_swagger',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
]

ENABLE_WHITENOISE = os.environ.get('ENABLE_WHITENOISE', 'on') == 'on' # Added for origin/openshift
if ENABLE_WHITENOISE:
    MIDDLEWARE_CLASSES.append('whitenoise.middleware.WhiteNoiseMiddleware')

MIDDLEWARE_CLASSES += [
    # Not needed as no UI is using this rest api
    # 'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # enabled for swagger
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restapi_project.urls'
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# enabled for swagger
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
from . import database
DATABASES = {
    'default': database.config()
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

# For Production set OS ENV PROJECT_LOGGING_LEVEL=WARNING
PROJECT_LOGGING_LEVEL = os.getenv('PROJECT_LOGGING_LEVEL', 'INFO')

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
            'level': PROJECT_LOGGING_LEVEL,
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'project_logging': {
            'handlers': ['console',],
            'level': PROJECT_LOGGING_LEVEL,
            'filters': ['require_debug_true']
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    # Not using IsAuthenticated because it blocks Swagger
    #'DEFAULT_PERMISSION_CLASSES': [
    #    'rest_framework.permissions.IsAuthenticated',
    #],
}

# Not needed as no UI is using this rest api
# CORS_ORIGIN_ALLOW_ALL = True

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

# For v0.9, updated v5.01
AWS_HTTP_PROXY = os.getenv('AWS_HTTP_PROXY')
AWS_HTTPS_PROXY = os.getenv('AWS_HTTPS_PROXY')

# For v0.11
# Enabled Templages, and other settings above, plus
SWAGGER_SETTINGS = {
    'VALIDATOR_URL': None,
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {},
}

# Status messaging
SUCCESS_MSG_NEW_BUCKET = os.getenv('SUCCESS_MSG_NEW_BUCKET', 'New bucket created')
SUCCESS_MSG_PREEXISTING_BUCKET = os.getenv('SUCCESS_MSG_PREEXISTING_BUCKET',
    'Bucket already exists')
AWS_NO_RESPONSE = os.getenv('AWS_NO_RESPONSE', 'AWS response is empty')

AWS_ACL_DEFAULT = os.getenv('ACL_DEFAULT', 'public-read')
AWS_ACL_CHOICES = os.getenv('AWS_ACL_CHOICES',
    'private|public-read|public-read-write|authenticated-read')
AWS_LOCATION_CONSTRAINT_CHOICES = os.getenv('AWS_LOCATION_CONSTRAINT_CHOICES',
    'EU|eu-west-1|us-west-1|us-west-2|ap-south-1|ap-southeast-1|ap-southeast-2|ap-northeast-1|sa-east-1|cn-north-1|eu-central-1')
AWS_BUCKET_NAME_COMPLIANT_MSG = os.getenv('AWS_BUCKET_NAME_MSG',
    'Bucket name is not DNS-compliant: http://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html')

# vi: ai et ts=4 sts=4 sw=4 nu ru
