import boto3
import logging

from botocore.vendored.requests.exceptions import ConnectionError
from django.conf import settings

logger = logging.getLogger('verbose_logging')

def create_s3_bucket(bucket, access_key, secret_key):
    """ Typical response

    {'ResponseMetadata':
        {'RequestId': '1C4B0BBDB5A4DE4C', 'HostId': 'IoS8NAfyHzgxqlE56Kw2pSCW1iNguFvlF0KCcU5VRmrCiIIfB71j5Oohpc0uyh3l/PWwYky5otM=', 'HTTPStatusCode': 200, 'HTTPHeaders':
          {'x-amz-id-2': 'IoS8NAfyHzgxqlE56Kw2pSCW1iNguFvlF0KCcU5VRmrCiIIfB71j5Oohpc0uyh3l/PWwYky5otM=', 'x-amz-request-id': '1C4B0BBDB5A4DE4C', 'date': 'Fri, 29 Sep 2017 06:06:40 GMT', 'location': '/Thur-27-2017', 'content-length': '0', 'server': 'AmazonS3'},
            'RetryAttempts': 0}, 'Location': '/Thur-27-2017'}
    """

    logger.info('Bucket:{}, AK: {}'.format(bucket,access_key))

    response = {}

    try:
        client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key)

        response = client.create_bucket(Bucket=bucket)

    except ConnectionError as e:
        logger.error('Connection Error: {}'.format(e))
        response = {'error': e}

    except Exception as e:
        logger.error('Exception: {}'.format(e))
        response = {'error': e}

    return response

# vim: ai et ts=4 sts=4 sw=4 ru nu
