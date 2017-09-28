# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# @python_2_unicode_compatible  # only if you need to support Python 2
class Server(models.Model):
    '''https://docs.djangoproject.com/en/1.11/ref/models/fields/#genericipaddressfield '''

    name = models.CharField(max_length=200, unique=True)
    ip = models.GenericIPAddressField(protocol='IPv4', unique=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return '{}:{}'.format(self.name, self.ip)

# vim: ai et ts=4 sts=4 sw=4 ru nu
