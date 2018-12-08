from django import template
from ..models import Story
from django.utils.html import format_html_join


register = template.Library()

@register.simple_tag
def story_to_story_connection_list(story_pairs):
    return format_html_join('',
                            "<li><div class='connection'><a href='{}'>{}</a> - <a href='{}'>{}</a></div></li>",
        ((s.story1.get_absolute_url(), s.story1.name,s.story2.get_absolute_url(), s.story2.name) for s in story_pairs)
    )

