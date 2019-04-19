from django import template
from django.utils.html import format_html_join
from .theme_list import theme_list


register = template.Library()

def submenu_item_name(string):
    # make a referrable html id from the theme name.
    # remove charcters that are incompatible
    return "submenu_"+string.replace(" ", "").replace("/","").replace("'","")

@register.simple_tag
def chain_with_theme_list(chains, connection_range):
    return format_html_join('',
                             "<div class='tc_block'> <h5>  <a href='{}' class='theme {}'>{}</a> <a href=\"#{}\" data-toggle=\"collapse\" aria-expanded=\"false\" class=\"dropdown-toggle\"></a> </h5> <div class=\"collapse\" id=\"{}\">{} </div> </div>",
                            #"<div class='tc_block'><h5><a href='{}' class='chain {}'>{}</a></h5>{}</div>",
        ((c.chain.get_absolute_url(), connection_range, c.chain.name, submenu_item_name(c.chain.name), submenu_item_name(c.chain.name), theme_list(c.themes, connection_range)) for c in chains)
    )

