from django import template
from django.utils.html import format_html_join
from .theme_inline_list import theme_inline_list


register = template.Library()

@register.simple_tag
def chain_with_theme_inline_list(chains):
    return format_html_join('',
                            "<div class='tc_block'><h5><a href='{}' class='chain'>{}</a></h5>{}</div>",
        ((c.chain.get_absolute_url(), c.chain.name, theme_inline_list(c.themes)) for c in chains)
    )

