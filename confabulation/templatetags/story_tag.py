from django import template
from ..models import Story
from ..utils.media_helpers import get_story_thumb
from django.utils.safestring import mark_safe


register = template.Library()

@register.simple_tag
def story_tag(story_id, size):
    story = Story.objects.get(pk=story_id)
    thumb = get_story_thumb(story, size)
    url = story.get_absolute_url()
    name = story.name
    return mark_safe("<a href='{url}'>{name}<img src='{thumb}'></a>".format(url=url, name=name, thumb=thumb))
