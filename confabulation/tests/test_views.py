from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from confabulation.models import Participant, ParticipantTypes, Gender

class ParticipantViewTestCase(TestCase):
    def setUp(self):
        self.participant = Participant(name="Test Bela",
                                       profile="test profile",
                                       participation_group=ParticipantTypes.photographer,
                                       gender=Gender.female,
                                       id=1)
        self.participant.save()

        User = get_user_model()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        self.client = Client()

    def test_participant_view(self):
        """partipant view can be rendered"""

        self.client.login(username='temporary', password='temporary')

        response = self.client.get(self.participant.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/participantView.html')
        self.assertContains(response, 'Test Bela')

class FrontPage(TestCase):
    def setUp(self):
        self.participant = Participant(name="Test Bela",
                                       profile="test profile",
                                       participation_group=ParticipantTypes.photographer,
                                       gender=Gender.female,
                                       id=1)
        self.participant.save()

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
