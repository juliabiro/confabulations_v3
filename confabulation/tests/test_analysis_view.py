from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .db_data import *
from ..models import Participant, Story

def AnalysisView(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')


def AnalysisTypeView(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')
