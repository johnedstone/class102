# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import binascii, logging, os, sys
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger('project_logging')

class Command(BaseCommand):
    help = """Set specific token for user.

    If user does not exist, creates user.first.
    """

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('token')
        

    def handle(self, *args, **options):
        try:
            u = User.objects.get(username=options['username'])

        except ObjectDoesNotExist:
            u = User()
            u.username = options['username']
            u.set_password(options['token'])
            u.full_clean()
            u.save()

        logger.info(u)

        if not hasattr(u, 'auth_token'):
            logger.info('Create token here')

        sys.exit()
        logger.info('{}: {}'.format(type(_token), _token.key))

        _token.delete()
        t = Token(user=u, key=options['token'])
        t.full_clean()
        t.save()
        logger.info('New token: {}'.format(u.auth_token.key))

'''
>>> binascii.hexlify(os.urandom(10)).decode()
'332b23fe41ea75c212f4'
>>> b = binascii.hexlify(os.urandom(10)).decode()
>>> u = User()
>>> u.username = 'HarryPotter'
>>> u.set_password(b)
>>> u.full_clean()
>>> u.save()
>>> u.auth_token
<Token: dd89e5127f4974a526a6af0be7a5f79d0b99fc6a>
>>> t = u.auth_token
>>> t.key
'dd89e5127f4974a526a6af0be7a5f79d0b99fc6a'
>>> t.delete()
(1, {'authtoken.Token': 1})
>>> t = Token(user=u, key=b)
>>> t.full_clean()
>>> t.save()
>>> u.auth_token
<Token: cf00edd60753f7608007>
'''

# vim: ai et ts=4 sw=4 sts=4 ru nu
