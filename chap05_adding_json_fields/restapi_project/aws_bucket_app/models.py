# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import re

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import (
    RegexValidator, MinLengthValidator,
)
from django.db import models
from django.db.models.signals import post_save

from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from .bucket import create_s3_bucket

logger = logging.getLogger('project_logging')

def validate_last_character(value):
    if value.endswith('.'):
        raise ValidationError(
            'Buckent name, %(value)s, can not have a trailing period - %(msg)s',
            params={
                'value': value,
                'msg': settings.AWS_BUCKET_NAME_COMPLIANT_MSG,
            },
        )

def validate_lowercase(value):
    patt = re.compile(r'[A-Z]')
    logger.info(patt.match(value))
    if patt.search(value):
        raise ValidationError(
            'Buckent name, %(value)s, can not have a upper case characters - %(msg)s',
            params={
                'value': value,
                'msg': settings.AWS_BUCKET_NAME_COMPLIANT_MSG,
            },
        )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    logger.info('Creating auth token')
    if created:
        Token.objects.create(user=instance)

class CreateBucket(models.Model):

    ACL_CHOICES = [(ac.strip(), ac.strip()) for ac in settings.AWS_ACL_CHOICES.split('|')]
    logger.info(ACL_CHOICES)

    LOCATION_CONSTRAINT_CHOICES = [(lc.strip(), lc.strip()) for lc in settings.AWS_LOCATION_CONSTRAINT.split('|')]
    logger.info(LOCATION_CONSTRAINT_CHOICES)

    acl = models.CharField(max_length=30, choices=ACL_CHOICES,
        default=settings.AWS_ACL_DEFAULT, blank=True)

    bucket = models.CharField(max_length=63, validators=[
        # This catches all, except 'ends with'
        # Ref: http://info.easydynamics.com/blog/aws-s3-bucket-name-validation-regex
        RegexValidator(
            regex='^([a-z]|(\d(?!\d{0,2}\.\d{1,3}\.\d{1,3}\.\d{1,3})))([a-z\d]|(\.(?!(\.|-)))|(-(?!\.))){1,61}[a-z\d\.]$',
            message=settings.AWS_BUCKET_NAME_COMPLIANT_MSG,
        ),
        validate_last_character,

        # The following are extra, and give more specific messages which are helpful
        MinLengthValidator(
            limit_value=3,
        ),
        validate_last_character,
        validate_lowercase,
    ])
    bucket_creation_date = models.CharField(max_length=30, default='',
        blank=True)
    change = models.CharField(max_length=25)
    client = models.ForeignKey(User, related_name="client",
        on_delete=models.CASCADE)
    dry_run = models.BooleanField(default=True, blank=True)
    location = models.CharField(max_length=255, default='', blank=True)
    location_constraint = models.CharField(max_length=30,
        choices=LOCATION_CONSTRAINT_CHOICES, default='', blank=True)
    new_bucket = models.CharField(max_length=10, default='unknown', blank=True)
    request_created =  models.DateTimeField(auto_now_add=True)
    request_modified = models.DateTimeField(auto_now=True)
    s3_response = JSONField(default={}, blank=True)
    s3_error = models.CharField(max_length=255, default='', blank=True)
    status = models.CharField(max_length=255, default='Pending', blank=True)

    def __str__(self):
        return '{}:{}:{}'.format(self.change, self.bucket, self.location)

    @property
    def http_status_code(self):
        return '{}'.format(self.s3_response.get(
            'ResponseMetadata', {}).get('HTTPStatusCode', 'unknown'))

    @property
    def amz_bucket_region(self):
        return '{}'.format(self.s3_response.get(
            'ResponseMetadata', {}).get('HTTPHeaders', {}).get('x-amz-bucket-region', 'unknown'))

    # Used to avoid dealing with User hyperlink
    @property
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
