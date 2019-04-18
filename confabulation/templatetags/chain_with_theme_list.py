from django import template
from django.utils.html import format_html_join
from .theme_list import theme_list


register = template.Library()

@register.simple_tag
def chain_with_theme_list(chains, connection_range):
    return format_html_join('',
                            "<div class='tc_block'><h5><a href='{}' class='chain {}'>{}</a></h5>{}</div>",
        ((c.chain.get_absolute_url(), connection_range, c.chain.name, theme_list(c.themes)) for c in chains)
    )

