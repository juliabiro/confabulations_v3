from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^participant/$', views.participants),
    url(r'^participant/(?P<participant_id>[0-9]+)/$', views.participant_view),
    url(r'^story/$', views.stories),
    url(r'^story/(?P<story_id>[0-9]+)/$', views.storyView),
    url(r'^thumbnails/$', views.thumbnails),
    url(r'^videos/$', views.videos),
    url(r'^videos/(?P<video_name>[A-Z]+[0-9]+)$', views.video_view),
    url(r'^eras/(?P<era_id>[0-9]+$)', views.era_view),
    url(r'^', views.index),
]
