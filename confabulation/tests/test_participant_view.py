from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .db_data import *
from ..models import Participant

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
        self.assertContains(response, 'elso story')
        self.assertContains(response, 'masodik story')
        self.assertContains(response, 'harmadik story')

        content=str(response.content)
        story_1_loc = content.find('elso story')
        story_2_loc = content.find('masodik story')
        story_3_loc = content.find('harmadik story')

        self.assertTrue(story_1_loc<story_3_loc)
        self.assertTrue(story_3_loc<story_2_loc)

