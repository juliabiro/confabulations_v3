from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import  Story, Era, AnalysisPoint
from ..utils.s3_helpers import *
from ..utils.media_helpers import get_story_thumb

def stories(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    story_list = Story.objects.all().order_by('name')
    context = {'story_list': story_list}
    context['sidebar'] = sidebar_context()
    return render(request, 'confabulation/stories.html', context)

## there is no ssearch on the html, so all necessary data needs to be here
def story_view(request, story_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    story = Story.objects.get(pk=story_id)
    participant = Participant.objects.get(pk=story.participant.id)
    analysis = story.analysis.all()
    video_url = story.video_url

    photos = []
    for p in story.photos.all():
        url = get_signed_photo_url(parse_key_from_url(p.file_url),
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
               'analysis':analysis,
               'photos': photos,
               'eras': story.era.all(),
               'keywords': story.keywords.all()
              }
    if video_url:
        try:
            url = get_signed_video_url(parse_key_from_url(video_url))
            if url:
                context['video_url'] = url

        except (ClientError, AttributeError):
            context["video_error_message"] = "The video at " + video_url + " doesn't exist."
    context['sidebar'] = sidebar_context()
    return render(request, 'confabulation/storyView.html', context)
