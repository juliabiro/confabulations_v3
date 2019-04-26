import re
from botocore.exceptions import ClientError
import boto3
from .data import S3_BUCKET, VIDEOS_DIR, CLOUDFRONT_DISTRIBUTION, CLOUDFRONT_KEY_ID, CLOUDFRONT_KEY_PATH
from datetime import datetime, timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
import os

def _gets3():

    # Get the service client.

    s3_client = boto3.client('s3')
    return s3_client

def rsa_signer(message):

    #with open(CLOUDFRONT_KEY_PATH, 'rb') as key_file:
    key = os.environ['CLOUDFRONT_KEY'].replace('\\r', '\r').replace('\\n', '\n')
    private_key = serialization.load_pem_private_key(
        data=key.encode('ascii'),
        password=None,
        backend=default_backend()
    )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def _getCloudFront():
   cloudfront_signer = CloudFrontSigner(CLOUDFRONT_KEY_ID, rsa_signer)
   return cloudfront_signer

def parse_key_from_url(url):
    return url.split("/")[-1]

def get_signed_video_url(file_name, raise_error=True):
    key = VIDEOS_DIR+file_name
    return get_signed_asset_link(key, raise_error)

def get_signed_photo_url(file_url, raise_error=True):
    try:
        key = file_url.split(S3_BUCKET)[-1].strip("/")
        return get_signed_asset_link(key, raise_error)

    except (AttributeError, ClientError) as e:
        if raise_error:
            raise e
        else:
            return None

def get_signed_asset_s3_link(key, raise_error=True):
    try:
        s3_client = _gets3()
        # this will raise an error if the key doesnt exists
        s3_client.head_object(Bucket=S3_BUCKET, Key=key)
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': key
            }
        )

        return url

    except ClientError as e:
        if raise_error:
            raise e
        else:
            print(e)
            print(key)
            return None

def get_signed_asset_link(key, raise_error=True):
    try:
        cloudfront_client = _getCloudFront()
        url= CLOUDFRONT_DISTRIBUTION + key
        expiry = datetime.now()+timedelta(hours=1)
        signed_url = cloudfront_client.generate_presigned_url(url, date_less_than=expiry)

        return signed_url

    except ClientError as e:
        if raise_error:
            raise e
        else:
            print(e)
            print(key)
            return None

def get_keys_with_prefix(prefix):
    s3_client = _gets3()
    response = s3_client.list_objects(Bucket=S3_BUCKET, Prefix=prefix)

    return list(map(lambda x: x['Key'], response['Contents'][1:]))
