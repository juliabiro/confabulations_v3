from ..models import Theme, Chain, Story, StoryToStoryConnection, Keyword, ThemeInChain

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

    def getChainlessThemes(self):
        all_themes = self.getThemes()
        all_chains = self.getChains()

        chained_theme_ids = set()
        for ch in all_chains:
            themes = ch.themes.distinct()

            for th in themes:
                chained_theme_ids.add(th.id)


        chainless_themes = []
        for th in all_themes.distinct():
            if th.id not in chained_theme_ids:
                chainless_themes.append(th)
        return chainless_themes

    def getStoryToStoryConnections(self):
        return list(StoryToStoryConnection.objects.filter(connection_range=self.connection_range).distinct())

    def buildchains(self, chains):
        participant_chains = []

        for chain in chains:
            themes = chain.themes.distinct().order_by('themeinchain__number')

            theme_list = self.buildthemes(themes)

            participant_chains.append(ChainWithThemes(chain, theme_list))
        return participant_chains

    def buildthemes(self, themes):
        themes_list = []
        for theme in themes:
            themes_list.append(ThemeWithStories(theme, theme.stories.distinct().order_by('storyintheme__number')))

        return themes_list


    def buildchainlessthemes(self):
        chainless_themes = self.getChainlessThemes()

        themes_list = []
        for th in chainless_themes:
                themes_list.append(th)


        return themes_list

    def buildstoryconnections(self):
        participant_stories = set()

        for q in self.getStoryToStoryConnections():
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
        return  Theme.objects.filter(stories__participant_id=self.participant_id, connection_range=self.connection_range).distinct().order_by('name')

    def getStories(self):
        return Story.objects.filter(participant_id=self.participant_id).distinct()

    def getStoryToStoryConnections(self):
        ret1 = StoryToStoryConnection.objects.filter(story1__participant_id=self.participant_id, connection_range=self.connection_range).distinct()
        ret2 = StoryToStoryConnection.objects.filter(story2__participant_id=self.participant_id, connection_range=self.connection_range).distinct()
        return list(ret1)+list(ret2)

    def buildthemes(self, themes):
        themes_list = []
        for theme in themes:
            themes_list.append(ThemeWithStories(theme, theme.stories.distinct().filter(participant_id=self.participant_id).order_by('storyintheme__number')))

        return themes_list

    def buildchainlessthemes(self):
        themes_list = []
        chainless_themes = self.getChainlessThemes()

        for theme in chainless_themes:
            themes_list.append(ThemeWithStories(theme, theme.stories.distinct().filter(participant_id=self.participant_id).order_by('storyintheme__number')))

        return themes_list


class UnconnectedStoryFinder():
    def __init__(self, participant_id):
        self.participant_id=participant_id
        self.intraBuilder=ParticipantConnectionBuilder(participant_id, 'Intraconnection')
        self.interBuilder=ParticipantConnectionBuilder(participant_id, 'Interconnection')

    def getThemes(self):
        return  Theme.objects.filter(stories__participant_id=self.participant_id).distinct().order_by('name')

    def getStories(self):
        return Story.objects.filter(participant_id=self.participant_id).distinct()

    def buildsinglestories(self):
        all_stories = self.getStories()

        # connected stories
        connected_story_pairs = self.intraBuilder.getStoryToStoryConnections() + self.interBuilder.getStoryToStoryConnections()

        connected_stories=[]
        for p in connected_story_pairs:
            connected_stories.append(p.story1)
            connected_stories.append(p.story2)


        # stories in themes
        themes_inter = self.interBuilder.buildthemes(self.getThemes())
        themes_intra= self.intraBuilder.buildthemes(self.getThemes())

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
