from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from .models import Participant, Story, Era, AnalysisPoint, AnalysisType
from .utils.s3_helpers import *

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    return render(request, 'frontpage.html')

def participants(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    participant_list = Participant.objects.all()
    context = {'participant_list':participant_list}
    return render(request, 'confabulation/participants.html', context)

def stories(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    story_list = Story.objects.all()
    context = {'story_list':story_list}
    return render(request, 'confabulation/stories.html', context)

#todo
#def analysisPoints(request)
#    pass


def participant_view(request, participant_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    participant = Participant.objects.get(pk=participant_id)
    participant_stories = Story.objects.filter(participant__id=participant_id)
    context = {'participant':participant, 'stories': participant_stories}
    return render(request, 'confabulation/participantView.html', context)


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

    return render(request, 'confabulation/storyView.html', context)

def thumbnails(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

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
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

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
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

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
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    era = Era.objects.get(pk=era_id)
    context = {
        'era': era
    }
    return render(request, 'confabulation/eraView.html', context)

def analysis_view(request, ap_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    ap = AnalysisPoint.objects.get(pk=ap_id)

    context = {
        'analysis_point': ap
    }

    return render(request, 'confabulation/analysisView.html', context)

def analysis_type_view(request, ap_type_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    ap_type = AnalysisType.objects.get(pk=ap_type_id)

    aps = AnalysisPoint.objects.filter(analysis_type_id=ap_type_id)

    context = {
        'analysis_type': ap_type,
        'analysis_points': aps
    }

    return render(request, 'confabulation/analysisTypeView.html', context)
