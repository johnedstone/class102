import os
import sys

from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))

# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
# Changed so that ALLOWED_HOSTS = ['*'] so we can run on 0.0.0.0 for demonstration,
#    not for production
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello World')

def boo_hoo(request):
    return HttpResponse('Boo Hoo!!')

def super_saiyans(request):
    return HttpResponse('Super Saiyans!! Defenders of Earth!!!  Protectors of the Dragonballs!!!!')

urlpatterns = (
    url(r'^$', index),
    url(r'^boo-hoo/$', boo_hoo),
    url(r'^super-saiyans/$', super_saiyans),
    url(r'^hello-world/$', index)
)


application = get_wsgi_application()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
