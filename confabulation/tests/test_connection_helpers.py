from django.test import TestCase
from .db_data import create_connections_data, PARTICIPANT_ID
from ..utils.connection_helpers import *
from ..models import Participant

class buildChains(TestCase):

    def setUp(self):
        create_connections_data()

    def test_build_inter_chains(self):
        chains = buildchains(participant_id=PARTICIPANT_ID, connection_range='Interconnection')
        self.assertEquals(len(chains), 1)
        self.assertEquals(chains[0].chain.name, 'Chain2')
        self.assertEquals(len(chains[0].themes), 2)
        self.assertEquals(chains[0].themes[0], 'Theme1')
        self.assertEquals(chains[0].themes[1], 'Theme3')


    def test_build_intra_chains(self):
        chains = buildchains(participant_id=PARTICIPANT_ID, connection_range='Intraconnection')
        self.assertEquals(len(chains), 1)
        self.assertEquals(chains[0].chain.name, 'Chain1')
        self.assertEquals(len(chains[0].themes), 2)
        self.assertEquals(chains[0].themes[0], 'Theme1')
        self.assertEquals(chains[0].themes[1], 'Theme2')

class buildThemes(TestCase):

    def setUp(self):
        create_connections_data()

    def test_build_inter_themes(self):
        themes=buildthemes(participant_id=PARTICIPANT_ID, connection_range='Interconnection')
        self.assertEquals(len(themes), 1)
        self.assertEquals(themes[0].theme.name, 'Theme3')
        self.assertEquals(len(themes[0].stories), 1)
        self.assertEquals(len(themes[0].stories[0].name), 'story2')

    def test_build_intra_themes(self):
        themes=buildthemes(participant_id=PARTICIPANT_ID, connection_range='Intraconnection')
        self.assertEquals(len(themes), 2)
        self.assertEquals(themes[0].theme.name, 'Theme1')
        self.assertEquals(themes[1].theme.name, 'Theme4')
        self.assertEquals(len(themes[0].stories), 2)
        self.assertEquals(len(themes[1].stories), 1)
        self.assertEquals(len(themes[0].stories[0].name), 'story1')
        self.assertEquals(len(themes[0].stories[1].name), 'story2')
        self.assertEquals(len(themes[1].stories[0].name), 'story5')

class buildSingleStories(TestCase):
    def setUp(self):
        create_connections_data()

    def test_build_single_story_list(self):
        self.fail()

class buildStoryToStoryConnections(TestCase):
    def setUp(self):
        create_connections_data()

    def test_build_storytostory_connection_list(self):
        self.fail()
