from django import template
from django.utils.html import format_html_join
from .story_list import story_list


register = template.Library()

def submenu_item_name(string):
    # make a referrable html id from the theme name.
    # remove charcters that are incompatible
    return "submenu_"+string.replace(" ", "").replace("/","").replace("'","")

@register.simple_tag
def theme_with_story_list(themes, connection_range):
    return  format_html_join('',
                             "<div class='theme {}' > <h6><a href='{}'>{}</a> <a href=\"#{}\" data-toggle=\"collapse\" aria-expanded=\"false\" class=\"dropdown-toggle theme-dropdown\" id='theme{}'></a></h6> <div class=\"collapse\" id=\"{}\">{} </div> </div>",
                            ((connection_range, t.theme.get_absolute_url(), t.theme.name,submenu_item_name(t.theme.name), t.theme.id, submenu_item_name(t.theme.name),  story_list(t.stories)) for t in themes)
    )

