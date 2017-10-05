# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import CreateBucket

class CreateBucketSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CreateBucket
        fields = [
            'bucket',
            'bucket_creation_date',
            'change',
            'client_id_display',
            'dry_run',
            'http_status_code',
            'location',
            'new_bucket',
            'request_created',
            's3_error',
            'status',
            'url',
            ]
        read_only_fields = [field for field in fields if field not in ['change', 'bucket', 'dry_run']]
        required = ['change', 'bucket']

# vim: ai et ts=4 sw=4 sts=4 ru nu 
