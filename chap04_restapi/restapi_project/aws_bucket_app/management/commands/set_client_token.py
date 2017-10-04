# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import binascii, logging, os, sys
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist, ValidationError

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

        try:
            if not hasattr(u, 'auth_token'):
                logger.info('Create token here')
                t = Token(user=u, key=options['token'])
                t.full_clean()
                t.save()
    
            t = u.auth_token
            logger.info('Prev token: {}, {}'.format(u.username, t.key))
    
            t.delete()
            t = Token(user=u, key=options['token'])
            t.full_clean()
            t.save()
            logger.info('New token: {}, {}'.format(u.username, t.key))

        except ValidationError as e:
            sys.stderr.write('{}\n'.format(e.messages))

# vim: ai et ts=4 sw=4 sts=4 ru nu
