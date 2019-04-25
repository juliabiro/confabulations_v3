import re
from botocore.exceptions import ClientError
import boto3
from .data import S3_BUCKET, VIDEOS_DIR
from datetime import datetime, timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner


def _gets3():

    # Get the service client.

    s3_client = boto3.client('s3')
    return s3_client

def rsa_signer(message):
    with open('/pk-APKAJ6OXE6IOMB4LF4FA.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def _getCloudFront():
   key_id = 'APKAJ6OXE6IOMB4LF4FA'
   cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)
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

def get_signed_asset_link(key, raise_error=True):
    try:
        #s3_client = _gets3()
        cloudfront_client = _getCloudFront()
        url='http://d3g74r7twa0u2z.cloudfront.net/'+S3_BUCKET+'/'+key
        expiry = datetime.now()+timedelta(hours=6)
        print(expiry)
        signed_url = cloudfront_client.generate_presigned_url(url, date_less_than=expiry)

        # this will raise an error if the key doesnt exists
        #cloudfront_client.head_object(Bucket=S3_BUCKET, Key=key)

        print(signed_url)
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
