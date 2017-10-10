# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import S3Bucket

class S3BucketSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = S3Bucket
        fields = [
            'acl',
            'amz_bucket_region',
            'bucket',
            'bucket_creation_date',
            'change',
            'client_id_display',
            'dry_run',
            'http_status_code',
            'location',
            'location_constraint',
            'new_bucket',
            'request_created',
            # 's3_response',
            's3_error',
            'status',
            'tag_set_list',
            'tag_set_created',
            'url',
            ]
        read_only_fields = [field for field in fields if field not in [
            'acl',
            'bucket',
            'change',
            'dry_run',
            'location_constraint',
            'tag_set_list',
            ]
        ]
        required = ['change', 'bucket']

# vim: ai et ts=4 sw=4 sts=4 ru nu 
