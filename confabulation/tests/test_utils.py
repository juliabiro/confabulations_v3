from django.test import TestCase
from botocore.exceptions import ClientError
from confabulation.utils.s3_helpers import *

class UtilTestCase(TestCase):
    def setUp(self):
        self.valid_video = "TEST/TEST01.mp4"
        self.valid_image = "TEST01.jpg"
        self.invalid_video = "BROKEN.mp4"
        self.invald_image = "BROKEN.jpg"
        self.malformed_image = "lowercase.jpg"

    def test_parse_key(self):
        ret = parse_key_from_url(self.valid_video)
        self.assertEquals(ret, "TEST01.mp4")

    def get_signed_video_url_valid(self):
        ret = get_signed_video_url(self.valid_video)
        self.assertEqual(ret, "https://s3-eu-west-1.amazonaws.com/confabulations/TEST/TEST01.mp4")

    def get_signed_video_url_invalid_error(self):
        self.assertRaises(ClientError,
                          get_signed_photo_url,
                          file_name=self.invalid_video,
                          raise_error=True)

    def get_signed_video_url_invalid_noerror(self):
        ret = get_signed_video_url(self.invalid_video, raise_error=False)
        self.assertNone(ret)

    def get_signed_photo_url_valid(self):
        ret = get_signed_photo_url(self.valid_photo)
        self.assertEqual(ret, "https://s3-eu-west-1.amazonaws.com/confabulations/TEST/i/TEST01.jpg")

    def get_signed_photo_url_invalid_error(self):
        self.assertRaises(ClientError,
                          get_signed_photo_url,
                          file_name=self.invalid_photo,
                          raise_error=True)

    def get_signed_photourl_invalid_noerror(self):
        ret = get_signed_photo_url(self.invalid_photo, raise_error=False)
        self.assertNone(ret)

    def get_signed_photo_url_malformed_error(self):
        self.assertRaises(ClientError,
                          get_signed_photo_url,
                          file_name=self.malformed_photo,
                          raise_error=True)

    def get_signed_photo_url_malformed_noerror(self):
        ret = get_signed_photo_url(self.malformed_photo,
                                   raise_error=False)
        self.assertNone(ret)
