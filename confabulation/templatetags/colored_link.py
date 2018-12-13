from django import template
from django.utils.html import format_html

register = template.Library()

# TODO; make all urls use get_absolute_url, dont construct
@register.simple_tag
def colored_link(text, color, url):
    return format_html(
        '<a href="{}" style="border-left: 10px solid {}; border-radius: 7px; padding: 2px; margin: 3px;">{}</a>', url, color, text
    )
