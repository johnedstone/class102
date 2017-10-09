# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 20:28
from __future__ import unicode_literals

import aws_bucket_app.models
from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateBucket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acl', models.CharField(blank=True, choices=[('private', 'private'), ('public-read', 'public-read'), ('public-read-write', 'public-read-write'), ('authenticated-read', 'authenticated-read')], default='public-read', max_length=30)),
                ('bucket', models.CharField(max_length=63, validators=[django.core.validators.RegexValidator(message='Bucket name is not DNS-compliant: http://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html', regex='^([a-z]|(\\d(?!\\d{0,2}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})))([a-z\\d]|(\\.(?!(\\.|-)))|(-(?!\\.))){1,61}[a-z\\d\\.]$'), aws_bucket_app.models.validate_last_character, django.core.validators.MinLengthValidator(limit_value=3), aws_bucket_app.models.validate_last_character, aws_bucket_app.models.validate_lowercase])),
                ('bucket_creation_date', models.CharField(blank=True, default='', max_length=30)),
                ('change', models.CharField(max_length=25)),
                ('dry_run', models.BooleanField(default=True)),
                ('location', models.CharField(blank=True, default='', max_length=255)),
                ('location_constraint', models.CharField(blank=True, choices=[('EU', 'EU'), ('eu-west-1', 'eu-west-1'), ('us-west-1', 'us-west-1'), ('us-west-2', 'us-west-2'), ('ap-south-1', 'ap-south-1'), ('ap-southeast-1', 'ap-southeast-1'), ('ap-southeast-2', 'ap-southeast-2'), ('ap-northeast-1', 'ap-northeast-1'), ('sa-east-1', 'sa-east-1'), ('cn-north-1', 'cn-north-1'), ('eu-central-1', 'eu-central-1')], default='', max_length=30)),
                ('new_bucket', models.CharField(blank=True, default='unknown', max_length=10)),
                ('request_created', models.DateTimeField(auto_now_add=True)),
                ('request_modified', models.DateTimeField(auto_now=True)),
                ('s3_response', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={})),
                ('s3_error', models.CharField(blank=True, default='', max_length=255)),
                ('status', models.CharField(blank=True, default='Pending', max_length=255)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
