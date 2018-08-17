from .s3_helpers import *
from ..models import Story

def get_story_thumb(story):
    if not story.photos:
        return None
    if story.photos.all().count() is 0:
        return None

    return get_signed_photo_url(parse_key_from_url(story.photos.all().first().file_url))
