from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from confabulation.models import Participant, ParticipantTypes, Gender, Story, Photo, AnalysisPoint, AnalysisType, Keyword, Era

ERAS = [Era(name="era1", id=1),
        Era(name="era2", id=2)]

PHOTOS = [Photo(name='photo1',
                file_url='photo_url_1',
                id=1),
          Photo(name='photo2',
                file_url='photo_url_2',
                id=2),
          Photo(name='photo3',
                file_url='photo_url_3',
                id=3)]

ANALYSIS_TYPES = [AnalysisType(name='analysis_type1',
                             id=1),
                AnalysisType(name='analysis_type2',
                             id=2)]

ANALYSIS_POINTS = [AnalysisPoint(name='analysis_point1',
                                 analysis_type=ANALYSIS_TYPES[0],
                                 id=1),
                   AnalysisPoint(name='analysis_point2',
                                 analysis_type=ANALYSIS_TYPES[1],
                                 id=2)]

PARTICIPANT = Participant(name="Test Bela",
                          profile="test profile",
                          participation_group=ParticipantTypes.photographer,
                          gender=Gender.female,
                          id=1)

KEYWORDS = [Keyword(name='keyword1', id=1),
            Keyword(name='keyword2', id=2),
            Keyword(name='keyword3', id=3)]

def populate_db():
    for e in ERAS:
        e.save()
    for p in PHOTOS:
        p.save()
    for at in ANALYSIS_TYPES:
        at.save()
    for ap in ANALYSIS_POINTS:
        ap.save()
    PARTICIPANT.save()
    for k in KEYWORDS:
        k.save()

class ParticipantView(TestCase):
    def setUp(self):
        populate_db()
        self.participant = Participant.objects.get(pk=1)

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

# class StoryView(TestCase):
#     def setUp(self):
#         self.story = Story(id=1,
#                            name="Test Bela",
#                            participant=PARTICIPANT,
#                            photos=PHOTOS,
#                            order_in_recording=2,
#                            video_url='video_url',
#                            analysis=ANALYSIS_POINTS,
#                            era=ERAS,
#                            notes="sometext",
#                            keywords=KEYWORDS
#         )
#         self.story.save()

#         User = get_user_model()
#         User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

#         self.client = Client()

#     def test_story_view(self):
#         response = self.client.get(self.story.get_absolute_url(id=1))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'confabulation/storyView.html')
#         self.assertContains(response, 'Test Bela')
#         self.assertContains(response, 'era1')
#         self.assertContains(response, 'keyword1')
#         self.assertContains(response, 'analysis_point1')
#         self.assertContains(response, 'photo_url1')
#         self.assertContains(response, 'video_url')


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

