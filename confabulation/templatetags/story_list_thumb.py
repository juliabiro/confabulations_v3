from django import template
from ..models import Story, Theme
from ..utils.media_helpers import get_story_thumb
from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join


register = template.Library()

def get_theme_list(story):
    tlist = []
    for t in Theme.objects.filter(stories__id=story.id):
        tlist.append('theme'+str(t.id))
    return ' '.join(tlist)

@register.simple_tag
def story_list_thumb(stories, size):
    return format_html_join('',
                            "<a href='{}' class='thumbnail {}'><img src='{}'><br>{}</a>",
        ((s.get_absolute_url(), get_theme_list(s), get_story_thumb(s, size), s.name) for s in stories)
    )
