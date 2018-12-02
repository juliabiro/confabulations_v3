from ..models import Theme, Chain, Story, StoryToStoryConnection

class ThemeWithStories():
    def __init__ (self, theme, stories):
        self.theme = theme
        self.stories = stories

class ChainWithThemes():
    def __init__(self, chain, themes):
        self.chain = chain
        self.themes = themes
class StoryPair():
    def __init__(self, story1, story2):
        self.story1=story1
        self.story2=story2


class ConnectionBuilder():
    def __init__(self, connection_range):
        self.connection_range=connection_range

    def getChains(self):
        return Chain.objects.filter(connection_range=self.connection_range).distinct().order_by('name')

    def getThemes(self):
        return Theme.objects.filter(connection_range=self.connection_range).distinct().order_by('name')

    def getStoryToStoryConnections(self):
        return StoryToStoryConnection.objects.filter(connection_range=self.connection_range).distinct().order_by('story1.name')

    def buildchains(self):
        participant_chains = []
        chains = self.getChains()
        # chains = Chain.objects.filter(themes__stories__participant_id=participant_id, connection_range=connection_range).distinct().order_by('name')

        for chain in chains:
            themes = chain.themes.distinct().order_by('name')

            story_list = []
            for theme in themes:
                story_list.append(ThemeWithStories(theme, theme.stories.distinct().order_by('name')))

            participant_chains.append(ChainWithThemes(chain, story_list))
        return participant_chains

    def buildthemes(self):
        participant_themes = []
        themes = self.getThemes()
        # themes = Theme.objects.filter(stories__participant_id=participant_id, connection_range=connection_range).distinct().order_by('name')
        for theme in themes:
            participant_themes.append(ThemeWithStories(theme, theme.stories.distinct().order_by('name')))

        return participant_themes

    def buildstoryconnections(self):
        participant_stories = set()

        # story_pairs1 = StoryToStoryConnection.objects.filter(story1__participant_id=participant_id, connection_range=connection_range).distinct()
        # story_pairs2 = StoryToStoryConnection.objects.filter(story2__participant_id=participant_id, connection_range=connection_range).distinct()

        # for qset in [story_pairs2, story_pairs1]:
        for qset in self.getStoryToStoryConnections():
            for q in qset:
                if q.story1.id<q.story2.id:
                    participant_stories.add((q.story1, q.story2))
                else:
                    participant_stories.add((q.story2, q.story1))

        return [StoryPair(q[0], q[1]) for q in (sorted(participant_stories, key=lambda x: x[0].id))]


class ParticipantConnectionBuilder(ConnectionBuilder):
    def __init__(self, participant_id, connection_range):
        self.participant_id=participant_id
        self.connection_range=connection_range

    def getChains(self):
        return Chain.objects.filter(themes__stories__participant_id=self.participant_id, connection_range=self.connection_range).distinct().order_by('name')

    def getThemes(self):
        return Theme.objects.filter(stories__participant_id=self.participant_id, connection_range=self.connection_range).distinct().order_by('name')

    def getStories(self):
        return Story.objects.filter(participant_id=self.participant_id).distinct()

    def getStoryToStoryConnections(self):
        ret1 = StoryToStoryConnection.objects.filter(story1__participant_id=self.participant_id, connection_range=self.connection_range).distinct()
        ret2 = StoryToStoryConnection.objects.filter(story2__participant_id=self.participant_id, connection_range=self.connection_range).distinct()
        return list(ret1)+list(ret2)

class UnconnectedStoryFinder():
    def __init__(self, participant_id):
        self.participant_id=participant_id
        self.intraBuilder=ParticipantConnectionBuilder(participant_id, 'Intraconnection')
        self.interBuilder=ParticipantConnectionBuilder(participant_id, 'Interconnection')

    def getStories(self):
        return Story.objects.filter(participant_id=self.participant_id).distinct()

    def buildsinglestories(self):
        all_stories = self.getStories()
        # all_stories = Story.objects.filter(participant_id=participant_id).distinct()

        # connected stories
        connected_story_pairs = self.intraBuilder.getStoryToStoryConnections() + self.interBuilder.getStoryToStoryConnections()
        # connected_story_pairs = self.buildstoryconnections(participant_id, 'Interconnection') + buildstoryconnections(participant_id, 'Intraconnection')

        connected_stories=[]
        for p in connected_story_pairs:
            connected_stories.append(p.story1)
            connected_stories.append(p.story2)


        # stories in themes
        themes_inter = self.interBuilder.buildthemes()
        themes_intra= self.intraBuilder.buildthemes()
        # themes_intra = buildthemes(participant_id, 'Intraconnection')
        # themes_inter = buildthemes(participant_id, 'Interconnection')

        for tcoll in themes_inter, themes_intra:
            for theme in tcoll:
                for story in theme.stories.filter(participant_id = self.participant_id):
                    connected_stories.append(story)

        connected_stories = sorted(set([s.id for s in connected_stories]))

        single_stories = []
        for s in all_stories:
            if s.id not in connected_stories:
                single_stories.append(s)

        return single_stories
