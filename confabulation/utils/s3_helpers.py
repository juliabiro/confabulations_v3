from botocore.exceptions import ClientError
import boto3

def _gets3():

    # Get the service client.

    s3_client = boto3.client('s3')
    return s3_client

def parse_key_from_url(url):
    return url.split("confabulations/")[-1]

def get_signed_asset_link(key, raise_error=True):
    try:
        s3_client = _gets3()

        # this will raise an error if the key doesnt exists
        s3_client.head_object(Bucket='confabulations', Key=key)

        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'confabulations',
                'Key': key
            }
        )

        return url
    except ClientError as e:
        if raise_error:
            raise e
        else:
            print(e)
            return None

def get_keys_with_prefix(prefix):
    s3_client = _gets3()
    response = s3_client.list_objects(Bucket='confabulations', Prefix=prefix)

    return list(map(lambda x: x['Key'], response['Contents'][1:]))
