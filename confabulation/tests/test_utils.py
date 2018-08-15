from botocore.exceptions import ClientError
from django.test import TestCase
from confabulation.utils.s3_helpers import *
from .db_data import *

class UtilTestCase(TestCase):
    def test_parse_key(self):
        ret = parse_key_from_url('/'+VALID_VIDEO_NAME)
        ret2 = parse_key_from_url('alma/'+VALID_VIDEO_NAME)
        self.assertEquals(ret, VALID_VIDEO_NAME)
        self.assertEquals(ret2, VALID_VIDEO_NAME)

    def get_signed_video_url_valid(self):
        ret = get_signed_video_url(VALID_VIDEO_NAME)
        self.assertEqual(ret, "https://s3-eu-west-1.amazonaws.com/confabulations/TEST/TEST01.mp4")

    def get_signed_video_url_invalid_error(self):
        self.assertRaises(ClientError,
                          get_signed_photo_url,
                          file_name=INVALID_VIDEO_NAME,
                          raise_error=True)

    def get_signed_video_url_invalid_noerror(self):
        ret = get_signed_video_url(INVALID_VIDEO_NAME, raise_error=False)
        self.assertNone(ret)

    def get_signed_photo_url_valid(self):
        ret = get_signed_photo_url(VALID_PHOTO_NAME)
        self.assertEqual(ret, "https://s3-eu-west-1.amazonaws.com/confabulations/TEST/i/TEST01.jpg")

    def get_signed_photo_url_invalid_error(self):
        self.assertRaises(ClientError,
                          get_signed_photo_url,
                          file_name=INVALID_PHOTO_NAME,
                          raise_error=True)

    def get_signed_photourl_invalid_noerror(self):
        ret = get_signed_photo_url(INVALID_PHOTO_NAME, raise_error=False)
        self.assertNone(ret)

    def get_signed_photo_url_malformed_error(self):
        self.assertRaises(AttributeError,
                          get_signed_photo_url,
                          file_name=MALFORMED_PHOTO_NAME,
                          raise_error=True)

    def get_signed_photo_url_missing_error(self):
        self.assertRaises(ClientError,
                          get_signed_photo_url,
                          file_name=MISSING_PHOTO_NAME,
                          raise_error=True)
