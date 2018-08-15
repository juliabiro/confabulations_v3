from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .db_data import *
from ..models import Participant, Story

class ParticipantView(TestCase):
    def setUp(self):
        populate_db()
        self.participant = Participant.objects.get(pk=1)
        self.participant.save()

        User = get_user_model()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        self.client = Client()
        self.client.login(username='temporary', password='temporary')

    def test_participant_view(self):
        """partipant view can be rendered"""

        response = self.client.get(self.participant.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/participantView.html')
        self.assertContains(response, 'Test Bela')

class StoryView(TestCase):
    def setUp(self):
        populate_db()

        User = get_user_model()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        self.client = Client()
        self.client.login(username='temporary', password='temporary')

    def test_story_view(self):
        story = Story.objects.get(pk=VALID_STORY_ID)
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(story.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/storyView.html')
        self.assertContains(response, 'Test Bela')
        self.assertContains(response, 'era1')
        self.assertContains(response, 'keyword1')
        self.assertContains(response, 'analysis_point1')
        self.assertContains(response, 'sometext')
        self.assertContains(response, VALID_PHOTO_NAME)
        self.assertContains(response, VALID_VIDEO_NAME)

    def test_story_view_invalid_media(self):
        story = Story.objects.get(pk=INVALID_STORY_ID)
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(story.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/storyView.html')
        self.assertContains(response, 'invalid notes')
        self.assertContains(response, INVALID_PHOTO_NAME+" doesn&#39;t exist")
        self.assertContains(response, MALFORMED_PHOTO_NAME+" doesn&#39;t exist")
        self.assertContains(response, MISSING_PHOTO_NAME+" doesn&#39;t exist")
        self.assertContains(response, INVALID_VIDEO_NAME+" doesn&#39;t exist")


class FrontPage(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        self.client = Client()

    def test_frontpage(self):
        """frontpage loads with contents and css"""
        self.client.login(username='temporary', password='temporary')

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontpage.html')
        self.assertContains(response, 'Bözsike')

        css_response = self.client.get('/static/css/style.css')
        self.assertEqual(css_response.status_code, 200)

    def test_frontpage_not_authenticated(self):
        """unauthenticated users get redirected"""
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')
