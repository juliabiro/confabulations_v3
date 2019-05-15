from django.conf.urls import url

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
    url(r'^participant/$', participants),
    url(r'^participant/(?P<participant_id>[0-9]+)/?$', participant_view),
    url(r'^story/$', stories),
    url(r'^story/(?P<story_id>[0-9]+)/?$', story_view),
    url(r'^eras/(?P<era_id>[0-9]+)/?$', era_view),
    url(r'^analysis/(?P<ap_id>[0-9]+)/?$', analysis_view),
    url(r'^analysis_type/(?P<ap_type_id>[0-9]+)/?$', analysis_type_view),
    url(r'^theme/$', themes),
    url(r'^theme/(?P<theme_id>[0-9]+)/?$', theme_view),
    url(r'^chain/$', chains),
    url(r'^chain/(?P<chain_id>[0-9]+)/?$', chain_view),
    url(r'^connects/(?P<connection_id>[0-9]+)/?$', connection_view),
    url(r'^image/(?P<image_name>[a-zA-Z0-9]+)/?$', image_view),
    url(r'^graph/(?P<participant_id>[0-9]+)/?$', graph_participant_view),
    url(r'^graph/?$', graph_view),
    url(r'^menumap/$', menumap),
    url(r'^search/', search_list_view),
    url(r'^', index),
]

