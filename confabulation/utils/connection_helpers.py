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
    participant_stories = set()
    story_pairs1 = StoryToStoryConnection.objects.filter(story1__participant_id=participant_id, connection_range=connection_range).distinct()
    story_pairs2 = StoryToStoryConnection.objects.filter(story2__participant_id=participant_id, connection_range=connection_range).distinct()

    for qset in [story_pairs2, story_pairs1]:
        for q in qset:
            if q.story1.id<q.story2.id:
                participant_stories.add((q.story1, q.story2))
            else:
                participant_stories.add((q.story2, q.story1))

    return [StoryPair(q[0], q[1]) for q in (sorted(participant_stories, key=lambda x: x[0].id))]

def buildsinglestories(participant_id):
    all_stories = Story.objects.filter(participant_id=participant_id).distinct()

    # connected stories
    connected_story_pairs = buildstoryconnections(participant_id, 'Interconnection') + buildstoryconnections(participant_id, 'Intraconnection')

    connected_stories=[]
    for p in connected_story_pairs:
        connected_stories.append(p.story1)
        connected_stories.append(p.story2)


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
