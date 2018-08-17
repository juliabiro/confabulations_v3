from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
import mock
from .db_data import *
from .utils_mock import mock_get_signed_asset_link
from ..models import Story

@mock.patch('confabulation.views.get_signed_photo_url', mock_get_signed_asset_link)
@mock.patch('confabulation.views.get_signed_video_url', mock_get_signed_asset_link)
class StoryView(TestCase):
    def setUp(self):
        populate_db()

        User = get_user_model()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        self.client = Client()
        self.client.login(username='temporary', password='temporary')

    def test_story_view(self):
        story = Story.objects.get(pk=VALID_STORY_ID)
        response = self.client.get(story.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/storyView.html')
        self.assertContains(response, 'Test Bela')
        self.assertContains(response, 'era1')
        self.assertContains(response, 'keyword1')
        self.assertContains(response, 'analysis_point1')
        analysis_link = '<a href="/analysis/{0}/">'.format(ANALYSIS_POINT_ID)
        self.assertContains(response, analysis_link)
        self.assertContains(response, 'sometext')
        self.assertContains(response, VALID_PHOTO_NAME)
        self.assertContains(response, VALID_VIDEO_NAME)

    def test_story_view_invalid_media(self):
        story = Story.objects.get(pk=INVALID_STORY_ID)
        response = self.client.get(story.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/storyView.html')
        self.assertContains(response, 'invalid notes')
        self.assertContains(response, INVALID_PHOTO_NAME+" doesn&#39;t exist")
        self.assertContains(response, MALFORMED_PHOTO_NAME+" doesn&#39;t exist")
        self.assertContains(response, MISSING_PHOTO_NAME+" doesn&#39;t exist")
        self.assertContains(response, INVALID_VIDEO_NAME+" doesn&#39;t exist")

