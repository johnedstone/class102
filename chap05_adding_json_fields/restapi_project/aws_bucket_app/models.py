# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from .bucket import create_s3_bucket

logger = logging.getLogger('project_logging')

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    logger.info('Creating auth token')
    if created:
        Token.objects.create(user=instance)

class CreateBucket(models.Model):
    ACL_CHOICES = (
        ('private', 'private'),
        ('public-read', 'public-read'),
        ('public-read-write', 'public-read-write'),
        ('authenticated-read', 'authenticated-read'),
    )

    LOCATION_CONSTRAINT = (
        ('EU', 'EU'),
        ('eu-west-1', 'eu-west-1'),
        ('us-west-1', 'us-west-1'),
        ('us-west-2', 'us-west-2'),
        ('ap-south-1', 'ap-south-1'),
        ('ap-southeast-1', 'ap-southeast-1'),
        ('ap-southeast-2', 'ap-southeast-2'),
        ('ap-northeast-1', 'ap-northeast-1'),
        ('sa-east-1', 'sa-east-1'),
        ('cn-north-1', 'cn-north-1'),
        ('eu-central-1', 'eu-central-1'),
    )

    acl = models.CharField(max_length=30, choices=ACL_CHOICES,
        default=settings.ACL_DEFAULT, blank=True)

    bucket = models.CharField(max_length=255)
    bucket_creation_date = models.CharField(max_length=30, default='',
        blank=True)
    change = models.CharField(max_length=25)
    client = models.ForeignKey(User, related_name="client",
        on_delete=models.CASCADE)
    dry_run = models.BooleanField(default=True, blank=True)
    location = models.CharField(max_length=255, default='', blank=True)
    location_constraint = models.CharField(max_length=30,
        choices=LOCATION_CONSTRAINT, default='', blank=True)
    new_bucket = models.CharField(max_length=10, default='unknown', blank=True)
    request_created =  models.DateTimeField(auto_now_add=True)
    request_modified = models.DateTimeField(auto_now=True)
    s3_response = JSONField(default={}, blank=True)
    s3_error = models.CharField(max_length=255, default='', blank=True)
    status = models.CharField(max_length=255, default='Pending', blank=True)

    def __str__(self):
        return '{}:{}:{}'.format(self.change, self.bucket, self.location)

    def http_status_code(self):
        return '{}'.format(self.s3_response.get(
            'ResponseMetadata', {}).get('HTTPStatusCode', 'unknown'))

    def amz_bucket_region(self):
        return '{}'.format(self.s3_response.get(
            'ResponseMetadata', {}).get('HTTPHeaders', {}).get('x-amz-bucket-region', 'unknown'))

    # Used to avoid dealing with User hyperlink
    def client_id_display(self):
        return '{}'.format(self.client.username)

    def save(self, *args, **kwargs):
        try:
            if self.dry_run:
                self.status = 'Dry Run'
                self.location = 'N/A'
            else:
                result = create_s3_bucket(
                    self.bucket, settings.AWS_ACCESS_KEY, 
                    settings.AWS_SECRET_KEY,
                    acl=self.acl,
                    location_constraint=self.location_constraint)

    
                if result:
                    self.bucket_creation_date = result.get('bucket_creation_date', '')
                    self.new_bucket = result.get('new_bucket', 'unknown')

                    _error = result.get('error')

                    if _error:
                        self.s3_error = _error
                        self.status = 'Failed'
                    else:
                        if self.new_bucket == 'yes':
                            self.status = settings.SUCCESS_MSG_NEW_BUCKET
                        elif self.new_bucket == 'no':
                            self.status = settings.SUCCESS_MSG_PREEXISTING_BUCKET
                        else:
                            self.status = 'unknown'

                        self.location = result.get('Location', '')
                        logger.info(type(result))
                        if isinstance(result, dict):
                            self.s3_response = result
                        logger.info('s3_response: {}'.format(self.s3_response))
                else:
                    self.status = settings.AWS_NO_RESPONSE

        except Exception as e:
            logger.error('Save Exception: {}'.format(e))

        super(CreateBucket, self).save(*args, **kwargs)


# vim: ai et ts=4 sw=4 sts=4 nu ru
