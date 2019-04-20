from django import template
from django.utils.html import format_html

register = template.Library()

# TODO; make all urls use get_absolute_url, dont construct
@register.simple_tag
def ap_link(text, color, url, description=None):
    return format_html(
        '<div class="taxonomy" style="border-left-color: {}; "> <a href="{}"  title="{}" data-placement="right">{}</a></div>', color, url,  description, text
    )
