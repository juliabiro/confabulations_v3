from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .db_data import populate_db, ANALYSIS_POINT_ID, ANALYSIS_TYPE_ID
from ..models import AnalysisPoint, AnalysisType

class AnalysisViews(TestCase):
    def setUp(self):

        populate_db()
        User = get_user_model()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def test_analysis_point_view(self):
        analysis_point = AnalysisPoint.objects.get(pk=ANALYSIS_POINT_ID)

        response = self.client.get(analysis_point.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/analysisView.html')
        self.assertContains(response, analysis_point.name)
        self.assertContains(response, analysis_point.description)
        self.assertContains(response, analysis_point.color_code)
        self.assertContains(response, analysis_point.analysis_type.name)
        self.assertContains(response, analysis_point.analysis_type.get_absolute_url())

    def test_analysis_type_view(self):
        ap_type = AnalysisType.objects.get(pk=ANALYSIS_TYPE_ID)

        response = self.client.get(ap_type.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/analysisTypeView.html')
        self.assertContains(response, ap_type.name)
        self.assertContains(response, ap_type.description)

        # i could do the lookup here too, but it would be repeating the program lgoic
        # instead just lets look for something that I know should be there
        ap = AnalysisPoint.objects.get(pk=ANALYSIS_POINT_ID)
        self.assertContains(response, ap.name)
        self.assertContains(response, "alma")
        self.assertContains(response, ap.get_absolute_url())

        content = str(response.content)
        print(content)
        self.assertTrue(content.find("alma")<content.find("analysis_point1"))


