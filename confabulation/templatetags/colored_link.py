from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def colored_link(text, color, url_prefix, url_id):
    return format_html(
        '<a href="{}{}/" style="border-left: 10px solid {}; border-radius: 7px; padding: 2px; margin: 3px;">{}</a>', url_prefix, url_id, color, text
    )
