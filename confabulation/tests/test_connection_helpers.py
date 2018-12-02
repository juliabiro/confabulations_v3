from django.test import TestCase
from .db_data import create_connections_data, PARTICIPANT_ID, OTHER_PARTICIPANT_ID
from ..utils.connection_helpers import ParticipantConnectionBuilder, ConnectionBuilder, UnconnectedStoryFinder
from ..models import Participant

class ConnectionBuilderTest(TestCase):
    pass

class ParticipantConnectionBuilderTest(TestCase):
    def setUp(self):
        create_connections_data()

    def test_build_inter_chains(self):
        chains = ParticipantConnectionBuilder(PARTICIPANT_ID, 'Interconnection').buildchains()
        self.assertEquals(len(chains), 1)
        self.assertEquals(chains[0].chain.name, 'Chain2')
        self.assertEquals(len(chains[0].themes), 2)
        self.assertEquals(chains[0].themes[0].theme.name, 'Theme1')
        self.assertEquals(chains[0].themes[1].theme.name, 'Theme3')


    def test_build_intra_chains(self):
        chains = ParticipantConnectionBuilder(PARTICIPANT_ID, 'Intraconnection').buildchains()
        self.assertEquals(len(chains), 1)
        self.assertEquals(chains[0].chain.name, 'Chain1')
        self.assertEquals(len(chains[0].themes), 2)
        self.assertEquals(chains[0].themes[0].theme.name, 'Theme1')
        self.assertEquals(chains[0].themes[1].theme.name, 'Theme2')

    def test_build_inter_themes(self):
        themes=ParticipantConnectionBuilder(PARTICIPANT_ID, 'Interconnection').buildthemes()
        self.assertEquals(len(themes), 1)
        self.assertEquals(themes[0].theme.name, 'Theme3')
        self.assertEquals(len(themes[0].stories), 2)
        self.assertEquals(themes[0].stories[0].name, 'story2')
        self.assertEquals(themes[0].stories[1].name, 'story3')

    def test_build_intra_themes(self):
        themes=ParticipantConnectionBuilder(PARTICIPANT_ID, 'Intraconnection').buildthemes()
        self.assertEquals(len(themes), 2)
        self.assertEquals(themes[0].theme.name, 'Theme1')
        self.assertEquals(themes[1].theme.name, 'Theme4')
        self.assertEquals(len(themes[0].stories), 2)
        self.assertEquals(len(themes[1].stories), 1)
        self.assertEquals(themes[0].stories[0].name, 'story1')
        self.assertEquals(themes[0].stories[1].name, 'story2')
        self.assertEquals(themes[1].stories[0].name, 'story5')

    def test_build_storytostory_connection_list(self):
        pairs = ParticipantConnectionBuilder(participant_id=PARTICIPANT_ID, connection_range='Interconnection').buildstoryconnections()
        self.assertEquals(len(pairs), 0)

        pairs = ParticipantConnectionBuilder(participant_id=PARTICIPANT_ID, connection_range='Intraconnection').buildstoryconnections()
        self.assertEquals(len(pairs),1)
        self.assertEquals(pairs[0].story1.name,'story1')
        self.assertEquals(pairs[0].story2.name,'story5')

        pairs = ParticipantConnectionBuilder(participant_id=PARTICIPANT_ID, connection_range='Interconnection').buildstoryconnections()
        self.assertEquals(len(pairs),0)


class UnconnectedStoryFinderTest(TestCase):
    def setUp(self):
        create_connections_data()

    def test_build_single_story_list(self):
        single_stories = UnconnectedStoryFinder(PARTICIPANT_ID).buildsinglestories()
        self.assertEquals(len(single_stories), 0)

        single_stories = UnconnectedStoryFinder(OTHER_PARTICIPANT_ID).buildsinglestories()
        self.assertEquals(len(single_stories), 1)
        self.assertEquals(single_stories[0].name, 'story6')


