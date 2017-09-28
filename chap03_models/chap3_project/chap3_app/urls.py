from django.conf.urls import url

from . import views
from .views import ServerList

urlpatterns = [
    url(r'^$', views.server_simple, name='server_simple'),
    url(r'^server-list/$', ServerList.as_view(), name='class_based_server_list'),
]
