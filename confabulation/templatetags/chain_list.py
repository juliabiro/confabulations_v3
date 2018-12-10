from django import template
from django.utils.html import format_html_join


register = template.Library()

@register.simple_tag
def chain_list(chains):
    return format_html_join(', ',
                            "<h5><a href='{}' class='chain'>{}</a></h5>",
        ((c.chain.get_absolute_url(), c.chain.name) for c in chains)
    )

