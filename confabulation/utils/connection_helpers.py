from ..models import Theme, Chain, Story, StoryToStoryConnection

class ChainsThemesStories():
    class ThemeWithStories():
        def __init__ (self, theme, stories):
            self.theme = theme
            self.stories = stories

    class ChainWithThemes():
        def __init__(self, chain, themes):
            self.chain = chain
            self.themes = themes

    def buildchains(self, participant_id, connection_range):
        participant_chains = []
        chains = Chain.objects.filter(themes__stories__participant_id=participant_id, connection_range=connection_range).distinct()

        for chain in chains:
            themes = chain.themes.all()

            story_list = []
            for theme in themes:
                story_list.append(self.ThemeWithStories(theme, theme.stories.all()))

            participant_chains.append(self.ChainWithThemes(chain, story_list))
        return participant_chains

    def buildthemes(self, participant_id, connection_range):
        participant_themes = []
        themes = Theme.objects.filter(stories__participant_id=participant_id, connection_range=connection_range).distinct()
        for theme in themes:
            participant_themes.append(self.ThemeWithStories(theme, theme.stories.all()))

        return participant_themes

    def buildstoryconnections(self, participant_id, connection_range):
        participant_stories = []
        story_pairs = StoryToStoryConnection.objects.filter(story1__participant_id=participant_id, connection_range=connection_range).distinct()
        for sp in story_pairs:
            participant_stories.append(sp.story1)
            participant_stories.append(sp.story2)

        return participant_stories
