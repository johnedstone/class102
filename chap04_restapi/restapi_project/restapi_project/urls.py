from django.conf.urls import url, include  
from django.http import HttpResponse
from django.shortcuts import redirect

from rest_framework.authtoken import views as drf_views

urlpatterns = [  
    url(r'^$', lambda x: redirect('/api/', permanent=False), name='home'),
    # url(r'^api/', include('aws_bucket_app.urls')),
    url(r'^liveness/', lambda request:HttpResponse(status=200)),
    url(r'^readiness/', lambda request:HttpResponse(status=200)),
]

urlpatterns += [
    # post with username and password to get token
    url(r'^api-token-auth/', drf_views.obtain_auth_token),
]

# vim: ai et ts=4 sw=4 sts=4 nu ru

