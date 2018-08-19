from sidebar import sidebar_context
from navbar import navigation_context

def setup_page_context(context=None, sidebar=True, navbar=True):
    if not context:
       context={}
    if sidebar:
        context['sidebar'] = sidebar_context()
    if navbar:
        context['navigation'] = navigation_context()
    return context

