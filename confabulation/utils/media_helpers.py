import cloudinary
import cloudinary.api
import cloudinary.utils
import cloudinary.uploader
from .s3_helpers import *
from ..models import Story
from django.conf import settings

def get_cloudinary_image_thumb(key):
    cloudinary.config(
    cloud_name = "dpn5pmgin",
    api_key = settings.CLOUDINARY_API_KEY,
    api_secret = settings.CLOUDINARY_API_SECRET
    )

    url=cloudinary.CloudinaryImage('confabulations/thumbnails/'+key+'.jpg').build_url( width=100, sign_url=True)
    return url

def get_story_thumb(story):
    if not story.photos:
        return None
    if story.photos.all().count() is 0:
        return None

    return get_signed_photo_url(parse_key_from_url(story.photos.all().first().file_url))
