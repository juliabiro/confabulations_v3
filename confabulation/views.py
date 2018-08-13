from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from .models import Participant, Story, Era
from .utils.s3_helpers import *

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    return render(request, 'frontpage.html')

def participants(request):
    participant_list = Participant.objects.all()
    context = {'participant_list':participant_list}
    return render(request, 'confabulation/participants.html', context)

def stories(request):
    story_list = Story.objects.all()
    context = {'story_list':story_list}
    return render(request, 'confabulation/stories.html', context)

#todo
#def analysisPoints(request)
#    pass


def participant_view(request, participant_id):
    participant = Participant.objects.get(pk=participant_id)
    participant_stories = Story.objects.filter(participant__id=participant_id)
    context = {'participant':participant, 'stories': participant_stories}
    return render(request, 'confabulation/participantView.html', context)


## there is no ssearch on the html, so all necessary data needs to be here
def storyView(request, story_id):
    story = Story.objects.get(pk=story_id)
    participant = Participant.objects.get(pk=story.participant.id)
    analysis = story.analysis.all()
    video_url = story.video_url
    photos = list(map(lambda p: {"name": p.name,
                                 "url": get_signed_photo_url(
                                     parse_key_from_url(p.file_url),
                                     raise_error=False)}, story.photos.all()))

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

        except ClientError:
            context["video_error_message"] = "The video at " + video_url + " doesnt exists"

    return render(request, 'confabulation/storyView.html', context)

def thumbnails(request):
    prefix = 'SG/pilot/thumbs'

    # Generate the URL to get 'key-name' from 'bucket-name'

    thumblist = []

    for key in get_keys_with_prefix(prefix):
        url = get_signed_asset_link(key)

        name = key.replace(prefix+'/', '').replace('\n', '')
        name = name[0:name.find('.')]
        thumblist.append({
            'name': name,
            'url': url
        })



    context = {
        'thumbnail_list':thumblist
    }

    return render(request, 'confabulation/thumbnails.html', context)

def videos(request):
    prefix = 'SG/pilot/SG_360'

    videolist = []
    for key in get_keys_with_prefix(prefix):
        url = get_signed_asset_link(key)

        videolist.append({
            'name': key.replace(prefix+'/', ""),
            'url': url
        })

        context = {
            'videos_list':videolist
        }

    return render(request, 'confabulation/videos.html', context)

def video_view(request, video_name):
    prefix = 'SG/pilot/SG_360'
    key = prefix+'/'+video_name
    url = get_signed_asset_link(key)

    context = {
        'video':{
            'name':video_name,
            'url':url
        }
    }

    return render(request, 'confabulation/videoView.html', context)

def era_view(request, era_id):
    era = Era.objects.get(pk=era_id)
    context = {
        'era': era
    }
    return render(request, 'confabulation/eraView.html', context)
