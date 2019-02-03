from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
import mock
from .utils_mock import mock_get_signed_asset_link

@mock.patch('confabulation.views.story_views.get_signed_video_url', mock_get_signed_asset_link)
class StaticPages(TestCase):
    def setUp(self):
        self.client = Client()

    def test_frontpage(self):
        """frontpage loads with contents and css"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontpage.html')

    def test_author(self):
        response = self.client.get('/author')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'author.html')

    def test_about(self): 
        response = self.client.get('/about')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_static_files(self):
        css_response = self.client.get('/static/mystyles.css')
        self.assertEqual(css_response.status_code, 200)
        css_response = self.client.get('/static/mystyles.js')
        self.assertEqual(css_response.status_code, 200)
