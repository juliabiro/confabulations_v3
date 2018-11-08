from ..models import Theme, Chain, Story, ConnectionRange

def get_chains_for_themes(themes, participant_id):
    chain_themes = {}
    chains = Chain.objects.filter(themes__name__in=themes).distinct()
    for c in chains:
        t = c.themes.filter(stories__participant__id=participant_id).distinct()
        chain_themes[c.name] = t
    return chain_themes

class ThemeWithStories():
    def __init__ (self, theme, stories):
        self.theme = theme
        self.stories = stories

def get_themes_for_stories(participant_id, connection_type):
    themes = Theme.objects.filter(stories__participant__id=participant_id, connection_range=connection_type).distinct()
    participant_themes=[]
    for theme in themes:
        participant_themes.append(ThemeWithStories(theme, theme.stories.all()))

    return participant_themes

