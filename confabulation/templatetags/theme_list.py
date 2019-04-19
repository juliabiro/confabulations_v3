from django import template
from django.utils.html import format_html_join


register = template.Library()

@register.simple_tag
def theme_list(themes, connection_range):
    return format_html_join('',
                            "<div class='tc_block'><a href='{}' class='theme {}'>{}</a></div>",
        ((t.theme.get_absolute_url(), connection_range, t.theme.name) for t in themes)
    )

