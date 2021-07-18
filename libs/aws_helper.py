import os
import uuid
from typing import Dict, List

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
from requests import post

s3_client = boto3.client('s3')
bckt_prfx = 'printerconnect'
bucket_name = os.environ['AWS_S3_BUCKET_NAME']


def create_bucket_name(bucket_prefix):
    """Generates a bucket name given a bucket prefix"""
    return ''.join([bucket_prefix, str(uuid.uuid4().int)[:10]])


def create_bucket(bucket_identifier, s3_connection, region: str = None):
    try:
        boto3.session.Session()
        if region is None:
            bucket_response = s3_connection.create_bucket(
                Bucket=bucket_identifier)
            return bucket_name, bucket_response
        else:
            bucket_response = s3_connection.create_bucket(
                Bucket=bucket_identifier,
                CreateBucketConfiguration={
                    'LocationConstraint': region
                }
            )
            return bucket_name, bucket_response

    except ClientError as e:
        return {'msg': str(e)}, 400
    except EndpointConnectionError as e:
        return {'msg': str(e)}, 400


def upload_file(file: str, bucket_identifier: str, file_name: str, client) -> bool:
    """
    Upload a file to an S3 bucket's object's folder using client.put_object()
    :param file: (Path to) file to upload
    :param bucket_identifier: Name of S3 bucket
    :param file_name: Name of file/key to upload to
    :param client: AWS S3 client
    """
    try:
        response = client.put_object(
            Body=file, Bucket=bucket_identifier, Key=file_name)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return response
    except ClientError:
        return False


def initialize_bucket(bucket_identifier, client):
    buckets = client.list_buckets()
    if len(buckets['Buckets']) == 0:
        create_bucket(bucket_identifier, client)
    for bucket in buckets['Buckets']:
        if bucket_name not in bucket['Name']:
            return create_bucket(bucket_identifier, client)

    return None


def cad_files_not_uploaded(client_files: List, client, client_folder):
    uploaded_objects = client.list_objects(
        Bucket=bucket_name, Prefix=client_folder)['Contents']
    # Create an empty list to append uploaded files
    not_uploaded = []
    # Loop through client files, append to not_uploaded if file is saved in S3
    if len(uploaded_objects) != 0:
        for client_file in client_files:
            uploaded = list(
                filter(lambda x: client_file in x['Key'], uploaded_objects))
            if len(uploaded) == 0:
                not_uploaded.append(client_file)
        return not_uploaded
    return client_files


def create_presigned_post_url(client, bucket_identifier, object_name, fields=None, conditions=None, expiration=3600):
    try:
        response = client.generate_presigned_post(
            Bucket=bucket_identifier,
            Key=object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration
        )
    except ClientError as e:
        return {'msg': str(e)}

    # The response contains the pre_signed URL and required fields
    return response


def create_presigned_url(client, bucket_identifier, object_name, expiration=3600):
    """
    Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
    except ClientError as e:
        return {'msg': str(e)}

    # The response contains the presigned URL
    return response


def post_with_presigned_url(url: str, data: Dict, file: str):
    try:
        response = post(url=url, data=data, files={'file': file})
    except Exception as e:
        return {'msg': str(e)}
    else:
        return response
