from .sidebar import sidebar_left_context, sidebar_right_context
from .navbar import navigation_context
import os

SITE_NAME = "Beyond The Photograph"
DEBUG_SITE_NAME = "LOCAL DB ALMA"

def setup_page_context(context=None, sidebar_left=False, sidebar_right=False, participant_id=None, navbar=True):
    if context is None:
       context={}
    if sidebar_left:
        context['sidebar_left'] = sidebar_left_context()
    if sidebar_right:
        context['sidebar_right'] = sidebar_right_context(participant_id)
    if navbar:
        context['navigation'] = navigation_context()
    if 'LOCAL' in os.environ:
        context['site_name'] = DEBUG_SITE_NAME
    else:
        context['site_name'] = SITE_NAME

    return context

