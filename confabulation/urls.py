from django.conf.urls import url

from .views.story_views import stories, story_view
from .views.participant_views import participants, participant_view
from .views.static_views import index, about, author, menumap
from .views.analysis_views import analysis_view, analysis_type_view
from .views.era_views import era_view

urlpatterns = [
    url(r'^participant/$', participants),
    url(r'^participant/(?P<participant_id>[0-9]+)/?$', participant_view),
    url(r'^story/$', stories),
    url(r'^story/(?P<story_id>[0-9]+)/?$', story_view),
    url(r'^eras/(?P<era_id>[0-9]+)/?$', era_view),
    url(r'^analysis/(?P<ap_id>[0-9]+)/?$', analysis_view),
    url(r'^analysis_type/(?P<ap_type_id>[0-9]+)/?$', analysis_type_view),
    url(r'^about/?$', about),
    url(r'^author/?$', author),
    url(r'^menumap/$', menumap),
    url(r'^', index),
]
