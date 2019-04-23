from django.test import TestCase
from ..models import ParticipantTypes, Participant, AnalysisType, AnalysisPoint
import mock
from .db_data import populate_db
from ..views.navbar import navigation_context

class NavigationContext(TestCase):

    def setUp(self):
        populate_db()

    def empty_query_set_participant(name="", participation_group=""):
        return Participant.objects.none()

    def empty_query_set_analysispoint(name="", analysis_type_id=""):
        return AnalysisPoint.objects.none()

    def empty_query_set_analysistype(name="", analysis_type_id=""):
        return AnalysisType.objects.none()

    def test_nav_context_initialized(self):
        context=navigation_context()
        for item in ['participants', 'taxonomy', 'confabulation']:
            self.assertTrue(item in context)

    def test_nav_context_full_db(self):
        context=navigation_context()
        self.assertTrue(len(context['participants']) > 0)
        for p in context['participants']:
            self.assertTrue(len(p) > 0)

        self.assertTrue(len(context['taxonomy']) > 0)
        for t in context['taxonomy']:
            self.assertTrue(len(t) > 0)

        self.assertTrue(len(context['confabulation']) > 0)
        for c in context['confabulation']:
            self.assertTrue(len(c) > 0)

        self.assertTrue(len(context['connects']) > 0)
        for c in context['connects']:
            self.assertTrue(len(c) > 0)

    @mock.patch('confabulation.views.navbar.Participant.objects.distinct', empty_query_set_participant)
    def test_nav_context_no_participants(self):
        context=navigation_context()
        self.assertTrue('participants' in context)
        self.assertEqual(context['participants'], [])

    @mock.patch('confabulation.views.navbar.AnalysisType.objects.all', empty_query_set_analysistype)
    def test_nav_context_no_analysys_types(self):
        context=navigation_context()
        self.assertTrue('taxonomy' in context)
        self.assertEqual(len(context['taxonomy']), 0)

    @mock.patch('confabulation.views.navbar.AnalysisPoint.objects.filter', empty_query_set_analysispoint)
    def test_nav_context_no_analysis_points(self):
        context=navigation_context()
        self.assertTrue('taxonomy' in context)
        self.assertTrue(len(context['taxonomy'])>0)
        for t in context['taxonomy']:
            self.assertEqual(len(context['taxonomy'][t]), 0)

    @mock.patch('confabulation.views.navbar.AnalysisType.objects.filter', empty_query_set_analysistype)
    def test_nav_context_no_Confabulation_type(self):
        context=navigation_context()
        self.assertTrue('confabulation' in context)
        self.assertEqual(len(context['confabulation']), 0)

    def test_nav_context_menu_order(self):
        context=navigation_context()
        confab_menu_items=context['confabulation']
        self.assertEquals(confab_menu_items[0]['name'], 'Long Confabulation')
        self.assertEquals(confab_menu_items[1]['name'], 'Short Confabulation')


