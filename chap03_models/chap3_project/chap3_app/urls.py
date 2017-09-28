from django.conf.urls import url

from . import views
from .views import ServerList

urlpatterns = [
    url(r'^$', views.server_simple, name='server_simple'),
    url(r'^server-list/$', ServerList.as_view(), name='class_based_server_list'),
]

# v0.4
from .views import ServerPrivateList

urlpatterns += [
    url(r'^private/$', ServerPrivateList.as_view(), name='private'),
]
