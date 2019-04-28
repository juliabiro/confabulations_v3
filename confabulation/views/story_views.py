from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from ..models import  Story, Era, AnalysisPoint, Participant, Keyword, StoryToStoryConnection, Theme
from ..utils.s3_helpers import *
from ..utils.connection_helpers import ParticipantConnectionBuilder
from .context_helpers import setup_page_context
from ..utils.story_sorter import sort_story_list
from ..utils.connection_helpers import ConnectionBuilder

def stories(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    story_list = sort_story_list(list(Story.objects.distinct()))
    connections = ConnectionBuilder('Intraconnection').buildstoryconnections()

    context = {'story_list': story_list, 'connections':connections}

    setup_page_context(context)
    return render(request, 'confabulation/stories.html', context)

## there is no ssearch on the html, so all necessary data needs to be here
def story_view(request, story_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    story = get_object_or_404(Story, pk=story_id)
    participant = get_object_or_404(Participant, pk=story.participant.id)
    analysis = story.analysis.distinct()
    video_url = story.video_url

    themes = Theme.objects.filter(stories__id=story_id).distinct()
    photos = []
    for p in story.photos.all():
        url = get_signed_photo_url(p.file_url,
                                   raise_error=False)
        if url is not None:
            photos.append(
                {"name": p.name,
                 "url": url
                })
        else:
            photos.append(
                {"name": p.name,
                 "photo_error_message": "the photo "+p.file_url+ " doesn't exist."
                })

    context = {'story': story,
               'participant':{
                   'name': participant.name,
                   'id': participant.id
               },
               'analysis':[{
                   'name': a.name,
                   'url': a.get_absolute_url,
                   'color_code': a.color_code,
                   'description': a.description,
               } for a in analysis],
               'photos': photos,
               'eras': [{
                   'name': era.name,
                   'color_code': era.color_code,
                   'url': era.get_absolute_url(),
                   'description': era.description
               } for era in story.era.distinct()],
               'keywords': story.keywords.all(),
               'themes': [{'name': t.name, 'url': t.get_absolute_url()} for t in themes]
              }
    if video_url:
        try:
            url = get_signed_video_url(parse_key_from_url(video_url))
            if url:
                context['video_url'] = url

        except (ClientError, AttributeError):
            context["video_error_message"] = "The video for " + parse_key_from_url(video_url) + " doesn't exist."

    story_pairs = ParticipantConnectionBuilder(participant.id, 'Intraconnection').buildstoryconnections()
    connected_stories = map(lambda s: s.story1 if int(story_id)==s.story2.id else s.story2, list((s for s in story_pairs if int(story_id) in (s.story1.id, s.story2.id))))

    context["connected_stories"] = connected_stories
    setup_page_context(context,
                       sidebar_right=True,
                       sidebar_left=True,
                       participant_id=participant.id)
    return render(request, 'confabulation/storyView.html', context)
