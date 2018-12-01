import cloudinary
import cloudinary.api
import cloudinary.utils
import cloudinary.uploader
from .s3_helpers import *
from ..models import Story
from .data import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, THUMBNAILS_PATH

def get_cloudinary_image_thumb(key):
    cloudinary.config(
    cloud_name = "dpn5pmgin",
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET
    )

    url=cloudinary.CloudinaryImage(THUMBNAILS_PATH +key+'.jpg').build_url( width=100, sign_url=True)
    return url

