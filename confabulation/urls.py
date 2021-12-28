from django.conf.urls import re_path

from .views.story_views import stories, story_view
from .views.participant_views import participants, participant_view
from .views.static_views import index, menumap
from .views.analysis_views import analysis_view, analysis_type_view
from .views.connection_view import connection_view
from .views.era_views import era_view
from .views.theme_view import themes, theme_view
from .views.chain_view import chains, chain_view
from .views.search_list_view import search_list_view
from .views.image_view import image_view
from .views.graph_view import graph_view, graph_participant_view

urlpatterns = [
    re_path(r'^participant/$', participants),
    re_path(r'^participant/(?P<participant_id>[0-9]+)/?$', participant_view),
    re_path(r'^story/$', stories),
    re_path(r'^story/(?P<story_id>[0-9]+)/?$', story_view),
    re_path(r'^eras/(?P<era_id>[0-9]+)/?$', era_view),
    re_path(r'^analysis/(?P<ap_id>[0-9]+)/?$', analysis_view),
    re_path(r'^analysis_type/(?P<ap_type_id>[0-9]+)/?$', analysis_type_view),
    re_path(r'^theme/$', themes),
    re_path(r'^theme/(?P<theme_id>[0-9]+)/?$', theme_view),
    re_path(r'^chain/$', chains),
    re_path(r'^chain/(?P<chain_id>[0-9]+)/?$', chain_view),
    re_path(r'^connects/(?P<connection_id>[0-9]+)/?$', connection_view),
    re_path(r'^image/(?P<image_name>[a-zA-Z0-9]+)/?$', image_view),
    re_path(r'^graph/(?P<participant_id>[0-9]+)/?$', graph_participant_view),
    re_path(r'^graph/?$', graph_view),
    re_path(r'^menumap/$', menumap),
    re_path(r'^search/', search_list_view),
    re_path(r'^', index),
]

