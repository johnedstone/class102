# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from django.dispatch import receiver
# from django.utils.encoding import python_2_unicode_compatible

from rest_framework.authtoken.models import Token

from .bucket import create_s3_bucket

logger = logging.getLogger('verbose_logging')

# @python_2_unicode_compatible
class RainbowColor(models.Model):

    created =  models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=25, unique=True)
    year_discovered = models.CharField(max_length=4)

    def __str__(self):
        return self.color

    def fullname(self):
        return '{}:{}'.format(self.color, self.year_discovered)


# @python_2_unicode_compatible
class DogBreed(models.Model):

    created =  models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    breed = models.CharField(max_length=25, unique=True)
    year_discovered = models.CharField(max_length=4, blank=False)

    def __str__(self):
        return self.color

    def fullname(self):
        return '{}:{}'.format(self.breed, self.year_discovered)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# @python_2_unicode_compatible
class CreateBucket(models.Model):

    created =  models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    change = models.CharField(max_length=25, unique=True)
    bucket = models.CharField(max_length=50, unique=True)
    http_status_code =  models.IntegerField(default=0)
    location = models.CharField(max_length=50, default='')
    s3_error = models.CharField(max_length=255, default='')
    status = models.CharField(max_length=10, default='Pending')

    def __str__(self):
        return '{}:{}:{}'.format(self.change, self.bucket, self.location)

    def save(self, *args, **kwargs):
        try:
            result = create_s3_bucket(
                self.bucket, settings.AWS_ACCESS_KEY, 
                settings.AWS_SECRET_KEY)

            if result:
                _error = result.get('error')
                if _error:
                    self.s3_error = _error
                    self.status = 'Failed'
                    self.http_status_code = result.get('http_status_code', 99)
                else:
                    self.status = 'Success'
                    self.location = result.get('location', '')
                    self.http_status_code = result.get('http_status_code', 98)

        except Exception as e:
            logger.error('Save Exception: {}'.format(e))


        
        super(CreateBucket, self).save(*args, **kwargs)


# vim: ai et ts=4 sw=4 sts=4 nu ru
