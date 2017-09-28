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


# v0.4
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Normally I would use https://django-braces.readthedocs.io/en/latest/index.html
# But let's use this decorator
@method_decorator(login_required, name='dispatch')
class ServerPrivateList(ListView):
    """ For tag v0.4 """
    model = Server
    template_name = 'chap3_app/private.html'

    # So how do we add extra content in this simplistic ListView
    # https://docs.djangoproject.com/en/1.11/topics/class-based-views/generic-display/#adding-extra-context

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ServerPrivateList, self).get_context_data(**kwargs)
        context['private_info'] = """You can't win, Darth. Strike me down, and I will become more powerful than you could possibly imagine."""
        return context

# vim: ai et ts=4 sts=4 sw=4 nu ru
