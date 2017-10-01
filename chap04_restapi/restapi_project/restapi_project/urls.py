from django.conf.urls import url, include  
from django.http import HttpResponse
from django.shortcuts import redirect

from rest_framework.authtoken import views as drf_views

urlpatterns = [  
    url(r'^$', lambda x: redirect('/api/', permanent=False), name='home'),
    url(r'^liveness/', lambda request:HttpResponse(status=200)),
    url(r'^readiness/', lambda request:HttpResponse(status=200)),
]

urlpatterns += [
    # post with username and password to get token
    url(r'^api-token-auth/', drf_views.obtain_auth_token),
]

# for v0.7 
from aws_bucket_app.urls import router as aws_bucket_router

urlpatterns += [
    # no name/namespace here
    url(r'^api/', include(aws_bucket_router.urls)),
]

# For v0.11
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Create AWS Bucket')

urlpatterns += [
    url(r'^swagger/$', schema_view)
]

# vim: ai et ts=4 sw=4 sts=4 nu ru
