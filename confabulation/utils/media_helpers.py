import cloudinary
import cloudinary.api
import cloudinary.utils
import cloudinary.uploader
from .data import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, THUMBNAILS_PATH, GRAPHS_PATH

def get_cloudinary_image_thumb(key, size):
    cloudinary.config(
    cloud_name = "dpn5pmgin",
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET
    )

    url=cloudinary.CloudinaryImage(THUMBNAILS_PATH +key+'.jpg').build_url( width=size, sign_url=True)
    return url

def get_story_thumb(story, size):
    return get_cloudinary_image_thumb(story.name, size)

def get_graph_url(participant_id, size=250):
    cloudinary.config(
    cloud_name = "dpn5pmgin",
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET
    )

    url=cloudinary.CloudinaryImage(GRAPHS_PATH+'small_graph_'+str(participant_id)+'.png').build_url( width=size, sign_url=True)

    return url
