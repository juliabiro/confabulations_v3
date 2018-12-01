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
    chains = Chain.objects.filter(themes__stories__participant_id=participant_id, connection_range=connection_range).distinct().order_by('name')

    for chain in chains:
        themes = chain.themes.distinct().order_by('name')

        story_list = []
        for theme in themes:
            story_list.append(ThemeWithStories(theme, theme.stories.distinct().order_by('name')))

        participant_chains.append(ChainWithThemes(chain, story_list))
    return participant_chains

def buildthemes(participant_id, connection_range):
    participant_themes = []
    themes = Theme.objects.filter(stories__participant_id=participant_id, connection_range=connection_range).distinct().order_by('name')
    for theme in themes:
        participant_themes.append(ThemeWithStories(theme, theme.stories.distinct().order_by('name')))

    return participant_themes

def buildstoryconnections(participant_id, connection_range):
    participant_stories = []
    story_pairs1 = [[sp.story1, sp.story2] for sp in StoryToStoryConnection.objects.filter(story1__participant_id=participant_id, connection_range=connection_range).distinct()]
    story_pairs2 = [[sp.story1, sp.story2] for sp in StoryToStoryConnection.objects.filter(story2__participant_id=participant_id, connection_range=connection_range).distinct()]

    for pair in story_pairs1+story_pairs2:
        participant_stories.append(tuple(sorted(pair, key=lambda s:s.id)))

    return list(set (participant_stories))

def buildsinglestories(participant_id):
    all_stories = Story.objects.filter(participant_id=participant_id).distinct()

    # connected stories
    connected_story_pairs = buildstoryconnections(participant_id, 'Interconnection') + buildstoryconnections(participant_id, 'Intraconnection')

    connected_stories=[]
    for p in connected_story_pairs:
        connected_stories.append(p[0])
        connected_stories.append(p[1])


    # stories in themes
    themes_intra = buildthemes(participant_id, 'Intraconnection')
    themes_inter = buildthemes(participant_id, 'Interconnection')

    for tcoll in themes_inter, themes_intra:
        for theme in tcoll:
            for story in theme.stories.filter(participant_id = participant_id):
                connected_stories.append(story)

    connected_stories = sorted(set([s.id for s in connected_stories]))

    single_stories = []
    for s in all_stories:
        if s.id not in connected_stories:
            single_stories.append(s)

    return single_stories
