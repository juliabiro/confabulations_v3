from .db_data import VALID_PHOTO_NAME, VALID_VIDEO_NAME
from ..utils.data import TAXONOMY_VIDEO_KEY

def mock_get_signed_asset_link(key, raise_error=True):
    if key == TAXONOMY_VIDEO_KEY:
        return "https://taxonomy_video_url/"

    if key in [VALID_VIDEO_NAME, VALID_VIDEO_NAME]:
        return "https://valid_url/TEST/"+key
    if raise_error:
        raise AttributeError
    return None
