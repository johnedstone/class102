import logging

from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView

logger = logging.getLogger('verbose_logging')

from .models import Server


def server_simple(request):
    server_list = Server.objects.order_by('-ip')[:5]
    context = {'server_list': server_list}
    logger.info(server_list)
    return render(request, 'chap3_app/server_list.html', context)

class ServerList(ListView):
    model = Server

# vim: ai et ts=4 sts=4 sw=4 nu ru
