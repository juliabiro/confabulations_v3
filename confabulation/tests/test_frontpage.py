from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model

class StaticPages(TestCase):
    def setUp(self):
        self.client = Client()

    def test_frontpage(self):
        """frontpage loads with contents and css"""
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontpage.html')

    def test_static_files(self):
        css_response = self.client.get('/static/mystyles.css')
        self.assertEqual(css_response.status_code, 200)
        css_response = self.client.get('/static/mystyles.js')
        self.assertEqual(css_response.status_code, 200)
