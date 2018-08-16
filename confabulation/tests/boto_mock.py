from botocore.exceptions import ClientError
from .db_data import VALID_PHOTO_NAME, VALID_VIDEO_NAME

def mock_head_object(Bucket, Key):
    if Key in [VALID_PHOTO_NAME, VALID_VIDEO_NAME]:
        return True
    raise ClientError

def mock_generate_presigned_url(ClientMethod, Params):
    return "https://valid.media.url/"+Paralms['Key']
