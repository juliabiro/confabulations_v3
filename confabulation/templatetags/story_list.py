from django import template
from ..models import Story
from ..utils.media_helpers import get_story_thumb
from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join


register = template.Library()

@register.simple_tag
def story_list(stories, size):
    return format_html_join('',
        "<a href='{}'>{}<img src='{}'></a>",
        ((s.get_absolute_url(), s.name, get_story_thumb(s, size)) for s in stories)
    )

