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
        self.assertEquals(chains[0].themes[0].theme.name, 'Theme1')
        self.assertEquals(chains[0].themes[1].theme.name, 'Theme3')


    def test_build_intra_chains(self):
        chains = buildchains(participant_id=PARTICIPANT_ID, connection_range='Intraconnection')
        self.assertEquals(len(chains), 1)
        self.assertEquals(chains[0].chain.name, 'Chain1')
        self.assertEquals(len(chains[0].themes), 2)
        self.assertEquals(chains[0].themes[0].theme.name, 'Theme1')
        self.assertEquals(chains[0].themes[1].theme.name, 'Theme2')

class buildThemes(TestCase):

    def setUp(self):
        create_connections_data()

    def test_build_inter_themes(self):
        themes=buildthemes(participant_id=PARTICIPANT_ID, connection_range='Interconnection')
        self.assertEquals(len(themes), 1)
        self.assertEquals(themes[0].theme.name, 'Theme3')
        self.assertEquals(len(themes[0].stories), 2)
        self.assertEquals(themes[0].stories[0].name, 'story2')
        self.assertEquals(themes[0].stories[1].name, 'story3')

    def test_build_intra_themes(self):
        themes=buildthemes(participant_id=PARTICIPANT_ID, connection_range='Intraconnection')
        self.assertEquals(len(themes), 2)
        self.assertEquals(themes[0].theme.name, 'Theme1')
        self.assertEquals(themes[1].theme.name, 'Theme4')
        self.assertEquals(len(themes[0].stories), 2)
        self.assertEquals(len(themes[1].stories), 1)
        self.assertEquals(themes[0].stories[0].name, 'story1')
        self.assertEquals(themes[0].stories[1].name, 'story2')
        self.assertEquals(themes[1].stories[0].name, 'story5')

class buildSingleStories(TestCase):
    def setUp(self):
        create_connections_data()

    def test_build_single_story_list(self):
        single_stories = buildsinglestories(PARTICIPANT_ID)
        self.assertEquals(len(single_stories), 0)

        single_stories = buildsinglestories(PARTICIPANT_ID+1)
        self.assertEquals(len(single_stories), 1)
        self.assertEquals(single_stories[0].name, 'story6')

class buildStoryToStoryConnections(TestCase):
    def setUp(self):
        create_connections_data()

    def test_build_storytostory_connection_list(self):
        pairs=buildstoryconnections(participant_id=PARTICIPANT_ID, connection_range='Interconnection')
        self.assertEquals(len(pairs), 0)

        pairs = buildstoryconnections(participant_id=PARTICIPANT_ID, connection_range='Intraconnection')
        self.assertEquals(len(pairs),1)
        self.assertEquals(pairs[0].story1.name,'story1')
        self.assertEquals(pairs[0].story2.name,'story5')

        pairs = buildstoryconnections(participant_id=PARTICIPANT_ID, connection_range='Interconnection')
        self.assertEquals(len(pairs),0)
