import re

def getmatchednumber(s):
    return str(int(s.group())).zfill(3)

def get_sortable_name(story):
    name = story.name
    sortable_name = re.sub(r'([\d]+)', getmatchednumber, name)
    return sortable_name

def sort_story_list(story_list):
    story_list.sort(key=get_sortable_name)
    return story_list
