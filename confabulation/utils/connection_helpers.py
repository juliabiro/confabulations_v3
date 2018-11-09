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

    def __init__(self, participant_id, connection_range):
        self.participant_id = participant_id
        self.connection_range = connection_range
        self.__populate()

    participant_chains = []


    def __populate(self):
        chains = Chain.objects.filter(themes__stories__participant_id=self.participant_id, connection_range=self.connection_range).distinct()

        for chain in chains:
            themes = chain.themes.all()

            story_list = []
            for theme in themes:
                story_list.append(self.ThemeWithStories(theme, theme.stories.all()))

            self.participant_chains.append(self.ChainWithThemes(chain, story_list))

    def __str__(self):

        data = "participant: "+ self.participant_id+"\n"+"connection range: "+ self.connection_range +"\n"
        chains = "Chains: \n"
        for c in self.participant_chains:
            cc = "  - "+ c.chain.name + "\n"

            chains = chains + cc
            themes = "  -- Themes: \n"
            for t in c.themes:
                tt = "  --- " + t.theme.name + "\n"
                themes = themes + tt

                stories = "  ---- Stories: \n"
                for s in t.stories:
                    ss = "  ----- "+s.name+"\n"
                    stories = stories + ss

                themes = themes + stories
            chains = chains + themes

        return data+chains
