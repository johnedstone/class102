from dateutil import tz
from django.conf import settings

# https://stackoverflow.com/questions/33480108/how-do-you-use-an-http-https-proxy-with-boto3
import botocore.endpoint
def _get_proxies(self, url):
    return {'http': settings.AWS_HTTP_PROXY, 'https': settings.AWS_HTTPS_PROXY}

botocore.endpoint.EndpointCreator._get_proxies = _get_proxies


import boto3
import logging

from botocore.vendored.requests.exceptions import ConnectionError

logger = logging.getLogger('project_logging')

NY_TIMEZONE = tz.gettz('America/New_York')

def create_s3_bucket(bucket, access_key, secret_key,
    acl=settings.AWS_ACL_DEFAULT,
    location_constraint=None):

    logger.info('Bucket:{}, AK: {}'.format(bucket,access_key))

    response = {}

    try:
        # http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.ServiceResource.create_bucket
        # http://boto3.readthedocs.io/en/latest/guide/migrations3.html#creating-the-connection 
        # http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.ServiceResource.buckets
        # http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.ServiceResource.create_bucket

        s3 = boto3.resource(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key)


        try:
            logger.info('Entering existing bucket try')
            response = s3.meta.client.head_bucket(Bucket=bucket)
            bucket_obj = s3.Bucket(bucket)
            response['bucket_creation_date'] = '{}'.format(
                bucket_obj.creation_date.astimezone(tz=NY_TIMEZONE))
            response['new_bucket'] = 'no'

        except botocore.exceptions.ClientError as e:
            logger.info('Entering new bucket create')
            logger.error(e)
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                if location_constraint:
                    new_bucket = s3.create_bucket(
                        Bucket=bucket,
                        ACL=acl,
                        CreateBucketConfiguration={
                           "LocationConstraint": location_constraint
                        }
                    )
                else:
                    new_bucket = s3.create_bucket(
                        Bucket=bucket,
                        ACL=acl
                    )

                response = s3.meta.client.head_bucket(Bucket=bucket)
                response['bucket_creation_date'] = '{}'.format(
                     new_bucket.creation_date.astimezone(tz=NY_TIMEZONE))
                response['new_bucket'] = 'yes'
            elif error_code == 403:
                response = {'error': e}
            else:
                raise

    except ConnectionError as e:
        logger.error('Connection Error: {}'.format(e))
        response = {'error': e}

    except Exception as e:
        logger.error('Bucket exception: {}'.format(e))
        response = {'error': e}

    logger.info(response)
    return response

# vim: ai et ts=4 sts=4 sw=4 ru nu
