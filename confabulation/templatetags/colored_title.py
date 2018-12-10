from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def colored_title(text, color):
    return format_html(
        '<h1 style="border-left: 15px solid {}; border-radius: 7px; padding: 2px; margin: 3px;">{}</h1>', color, text
    )
