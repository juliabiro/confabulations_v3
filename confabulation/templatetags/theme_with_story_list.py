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
                             "<div class='tc_block'> <h5>  <a href='{}' class='theme {}'>{}</a> <a href=\"#{}\" data-toggle=\"collapse\" aria-expanded=\"false\" class=\"dropdown-toggle\"></a> </h5> <div class=\"collapse\" id=\"{}\">{} </div> </div>",
                            ((t.theme.get_absolute_url(), connection_range, t.theme.name,submenu_item_name(t.theme.name),  submenu_item_name(t.theme.name), story_list(t.stories)) for t in themes)
    )

