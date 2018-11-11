from ..models import Theme, Chain, Story, StoryToStoryConnection

class ThemeWithStories():
    def __init__ (self, theme, stories):
        self.theme = theme
        self.stories = stories

class ChainWithThemes():
    def __init__(self, chain, themes):
        self.chain = chain
        self.themes = themes

def buildchains(participant_id, connection_range):
    participant_chains = []
    chains = Chain.objects.filter(themes__stories__participant_id=participant_id, connection_range=connection_range).distinct()

    for chain in chains:
        themes = chain.themes.all()

        story_list = []
        for theme in themes:
            story_list.append(ThemeWithStories(theme, theme.stories.all()))

        participant_chains.append(ChainWithThemes(chain, story_list))
    return participant_chains

def buildthemes(participant_id, connection_range):
    participant_themes = []
    themes = Theme.objects.filter(stories__participant_id=participant_id, connection_range=connection_range).distinct()
    for theme in themes:
        participant_themes.append(ThemeWithStories(theme, theme.stories.all()))

    return participant_themes

def buildstoryconnections(participant_id, connection_range):
    participant_stories = []
    story_pairs = StoryToStoryConnection.objects.filter(story1__participant_id=participant_id, connection_range=connection_range).distinct()
    for sp in story_pairs:
        participant_stories.append(sp.story1)
        participant_stories.append(sp.story2)

    return participant_stories

def buildsinglestories(participant_id):
    all_stories = Story.objects.filter(participant_id=participant_id).distinct()
    themes = Theme.objects.filter(stories__participant_id=participant_id)
    conns1 = StoryToStoryConnection.objects.filter(story1__participant_id=participant_id)
    conns2 = StoryToStoryConnection.objects.filter(story2__participant_id=participant_id)

    connected_stories = []
    for theme in themes:
        for s in theme.stories.distinct():
            connected_stories.append(s.id)
        for c in conns1.append(conns2):
            print(c)
            connected_stories.append(c.story1.id)

    print (connected_stories)
    single_stories = []
    for s in all_stories:
        if s.id not in connected_stories:
            single_stories.append(s)

    return single_stories
