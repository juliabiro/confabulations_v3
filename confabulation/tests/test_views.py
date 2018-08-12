from django.test import TestCase
from django.test import Client
from confabulation.models import Story, Participant, ParticipantTypes, Gender


class ParticipantViewTestCase(TestCase):
    def setUp(self):
        Participant.obkects.create(name="Test Bela",
                                   profile="test profile",
                                   participation_group=ParticipantTypes.photographer,
                                   gender=Gender.female
        )
        self.client = Client()

    def test_participant_view(self):
        """partipant view can be rendered"""
        url = 'participant/1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'participantView.html')
        self.assertContains(response, 'Test Bela')
        self.assertContains(response, 'Test Geza')

