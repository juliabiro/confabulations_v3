from .db_data import VALID_PHOTO_NAME, VALID_VIDEO_NAME

def mock_get_signed_asset_link(key, raise_error=True):
    if key in [VALID_VIDEO_NAME, VALID_VIDEO_NAME]:
        return "https://valid_url/TEST/"+key
    if raise_error:
        raise AttributeError
    return None
