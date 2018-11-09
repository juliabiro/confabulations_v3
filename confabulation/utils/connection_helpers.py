from ..models import Theme, Chain, Story

class ChainsThemesStories():
    class ThemeWithStories():
        def __init__ (self, theme, stories):
            self.theme = theme
            self.stories = stories

    class ChainWithThemes():
        def __init__(self, chain, themes):
            self.chain = chain
            self.themes = themes

    def build(self, participant_id, connection_range):
        participant_chains = []
        chains = Chain.objects.filter(themes__stories__participant_id=participant_id, connection_range=connection_range).distinct()

        for chain in chains:
            themes = chain.themes.all()

            story_list = []
            for theme in themes:
                story_list.append(self.ThemeWithStories(theme, theme.stories.all()))

            participant_chains.append(self.ChainWithThemes(chain, story_list))
        return participant_chains
