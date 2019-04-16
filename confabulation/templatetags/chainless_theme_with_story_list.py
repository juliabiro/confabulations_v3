from django import template
from django.utils.html import format_html_join
from .story_list import story_list


register = template.Library()

@register.simple_tag
def chainless_theme_with_story_list(themes):
    return format_html_join('',
                            "<div class='tc_block'> <h5>  <a href='{}' class='theme'>{}</a>  </h5> <div >{} </div> </div>",
                            ((t.theme.get_absolute_url(), t.theme.name, story_list(t.stories)) for t in themes)
    )
