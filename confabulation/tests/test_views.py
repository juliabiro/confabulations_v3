from django.test import TestCase
from django.test import Client
from django.urls import reverse
from confabulation.models import Story, Participant, ParticipantTypes, Gender
from confabulation.views import *

class ParticipantViewTestCase(TestCase):
    def setUp(self):
        self.participant = Participant(name="Test Bela",
                                       profile="test profile",
                                       participation_group=ParticipantTypes.photographer,
                                       gender=Gender.female,
                                       id=1)
        self.participant.save()
        self.client = Client()

    def test_participant_view(self):
        """partipant view can be rendered"""
        response = self.client.get(self.participant.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/participantView.html')
        self.assertContains(response, 'Test Bela')
