import re

def get_sortable_number(story):
    name = story.name
    m = re.search('\d+', name)
    if m:
        match = m.group()
        return int(match)
    return name

def sort_story_list(story_list):
    story_list.sort(key=get_sortable_number)
    return story_list
