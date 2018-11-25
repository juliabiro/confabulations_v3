import cloudinary
import cloudinary.api
import cloudinary.utils
import cloudinary.uploader
from .s3_helpers import *
from ..models import Story


def get_cloudinary_image(key):
    cloudinary.config(
    cloud_name = "dpn5pmgin",
    api_key = "314756966717226",
    api_secret = "n4ezvHLdz5p5X3FJ30TN2xS6Fhc"
    )

    # ret=cloudinary.uploader.upload('s3://confabulations'+key, upload_preset='wm9ze7cu', type="private", public_id='confabulations'+key)
    # print(ret)
    url=cloudinary.CloudinaryImage('confabulations'+key).build_url( width=100, sign_url=True)
    print (url)
    return url

def get_story_thumb(story):
    if not story.photos:
        return None
    if story.photos.all().count() is 0:
        return None

    return get_signed_photo_url(parse_key_from_url(story.photos.all().first().file_url))
