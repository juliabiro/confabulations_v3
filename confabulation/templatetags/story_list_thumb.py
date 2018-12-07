from django import template
from ..models import Story
from ..utils.media_helpers import get_story_thumb
from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join


register = template.Library()

@register.simple_tag
def story_list_thumb(stories, size):
    return format_html_join('',
                            "<div class='thumbnail'><a href='{}'><img src='{}'><br>{}</a></div>",
        ((s.get_absolute_url(), get_story_thumb(s, size), s.name) for s in stories)
    )
