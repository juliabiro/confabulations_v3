from django import template
from django.utils.html import format_html_join


register = template.Library()

@register.simple_tag
def theme_list(themes):
    return format_html_join('',
                            "<a href='{}' class='theme'>{}</a>",
        ((t.theme.get_absolute_url(), t.theme.name) for t in themes)
    )

