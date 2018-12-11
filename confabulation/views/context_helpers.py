from .sidebar import sidebar_context
from .navbar import navigation_context
import os

def setup_page_context(context=None, sidebar_participants=True, sidebar_taxonomy=True, navbar=True):
    if not context:
       context={}
    context['sidebar'] = sidebar_context(sidebar_participants, sidebar_taxonomy)

    if navbar:
        context['navigation'] = navigation_context()
    if 'LOCAL' in os.environ:
        context['debug'] = True
    return context

