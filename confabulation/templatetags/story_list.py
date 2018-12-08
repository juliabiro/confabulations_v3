from django import template
from ..models import Story
from ..utils.media_helpers import get_story_thumb
from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join


register = template.Library()

@register.simple_tag
def story_list(stories):
    return format_html_join(' ',
                            "<a href='{}' class='story'>{}</a>",
        ((s.get_absolute_url(), s.name) for s in stories)
    )

