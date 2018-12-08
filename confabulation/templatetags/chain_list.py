from django import template
from django.utils.html import format_html_join


register = template.Library()

@register.simple_tag
def chain_list(chains):
    return format_html_join(', ',
                            "<div class='chain'><h5><a href='{}'>{}</a></h5></div>",
        ((c.chain.get_absolute_url(), c.chain.name) for c in chains)
    )

