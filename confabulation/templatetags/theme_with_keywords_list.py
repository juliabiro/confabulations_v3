from django import template
from django.utils.html import format_html_join


register = template.Library()



def get_keywords(theme):
    keywords = []
    for s in list(theme.stories):
        for k in list(s.keywords.distinct()):
            keywords.append(k.name)
    return list(sorted(set(keywords)))

@register.simple_tag
def theme_with_keywords_list(themes):
    return format_html_join('',
                            "<div class='col-2 p2'><div class='theme'><a href='{}'>{}</a></div><br> <b>Keywords:</b> <div class='keyword'>{}</div></div>",
        ((t.theme.get_absolute_url(), t.theme.name, ', '.join( get_keywords(t))) for t in themes)
    )

