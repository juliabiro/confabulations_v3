from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .db_data import populate_db, THEME_INTER_ID, THEME_INTRA_ID, CHAIN_INTER_ID, CHAIN_INTRA_ID
from ..models import Theme, Chain

class Themes(TestCase):
    def setUp(self):
        populate_db()
        User = get_user_model()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def test_theme_view_inter(self):
        theme = Theme.objects.get(id=THEME_INTER_ID)
        response = self.client.get(theme.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/themeView.html')
        self.assertContains(response, theme.name)
        self.assertContains(response, 'Inter-connection')
        self.assertContains(response, 'elso story')
        self.assertContains(response, 'external story')
        self.assertContains(response, 'Chain 1')

    def test_theme_view_intra(self):
        theme = Theme.objects.get(id=THEME_INTRA_ID)
        response = self.client.get(theme.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/themeView.html')
        self.assertContains(response, theme.name)
        self.assertContains(response, 'Intra-connection')
        self.assertContains(response, 'elso story')
        self.assertContains(response, 'harmadik story')
        self.assertContains(response, 'Chain 2')

class Chains(TestCase):
    def setUp(self):
        populate_db()
        User = get_user_model()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def test_chain_view_inter(self):
        theme = Chain.objects.get(id=CHAIN_INTER_ID)
        response = self.client.get(theme.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/chainView.html')
        self.assertContains(response, theme.name)
        self.assertContains(response, 'Inter-connection')
        self.assertContains(response, 'Theme 1')

    def test_chain_view_intra(self):
        theme = Chain.objects.get(id=CHAIN_INTRA_ID)
        response = self.client.get(theme.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confabulation/chainView.html')
        self.assertContains(response, theme.name)
        self.assertContains(response, 'Intra-connection')
        self.assertContains(response, 'Theme 2')
        self.assertContains(response, 'Theme 3')
