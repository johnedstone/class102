from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'servers/', include('chap3_app.urls', namespace='servers')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

## Added for v0.4
from django.contrib.auth import views as auth_views
urlpatterns += [
    # https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
]

## Added for v0.5


from django.http import HttpResponse
from django.views.generic.base import RedirectView


urlpatterns += [
    url(r'^health/$', lambda request:HttpResponse(status=200)),
    url(r'^liveness/$', lambda request:HttpResponse(status=200)),
    url(r'^$',
        RedirectView.as_view(pattern_name='servers:server_simple', permanent=False),
                                                         name='home'),
]
# vim: ai et ts=4 sts=4 sw=4 nu ru
