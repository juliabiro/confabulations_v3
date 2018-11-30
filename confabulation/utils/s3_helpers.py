import re
from botocore.exceptions import ClientError
import boto3
from .data import S3_BUCKET

def _gets3():

    # Get the service client.

    s3_client = boto3.client('s3')
    return s3_client

def parse_key_from_url(url):
    return url.split("/")[-1]

def get_signed_video_url(file_name, raise_error=True):
    key = VIDEOS_DIR+file_name
    return get_signed_asset_link(key, raise_error)

def get_signed_photo_url(file_name, raise_error=True):
    m = re.match('^[A-Z]+', file_name)
    try:
        key = m.group(0)+"/i/"+file_name
        return get_signed_asset_link(key, raise_error)

    except (AttributeError, ClientError) as e:
        if raise_error:
            raise e
        else:
            return None

def get_signed_asset_link(key, raise_error=True):
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

def get_keys_with_prefix(prefix):
    s3_client = _gets3()
    response = s3_client.list_objects(Bucket=S3_BUCKET, Prefix=prefix)

    return list(map(lambda x: x['Key'], response['Contents'][1:]))
