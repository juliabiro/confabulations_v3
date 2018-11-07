from ..models import Theme, Chain, Story

def get_themes_for_stories(participant_stories, participant_id):
    theme_stories = {}
    for story in participant_stories:
        themes = Theme.objects.filter(stories=story)
        for t in themes:
            s = t.stories.filter(participant__id=participant_id)
            theme_stories[t.name] = s
    return theme_stories

def get_chains_for_themes(themes, participant_id):
    chain_themes = {}
    chains = Chain.objects.filter(themes__name__in=themes).distinct()
    for c in chains:
        t = c.themes.filter(stories__participant__id=participant_id).distinct()
        chain_themes[c.name] = t
    return chain_themes

