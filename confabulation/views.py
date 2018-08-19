from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from .models import Participant, Story, Era, AnalysisPoint, AnalysisType
from .models import ParticipantTypes
from .utils.s3_helpers import *
from .utils. media_helpers import get_story_thumb

# Create your views here.
def index(request):
    return render(request, 'frontpage.html')

def about(request):
    return render(request, 'about.html')

def author(request):
    return render(request, 'author.html')

# todo move this out from here
def sidebar_context():
    participants = Participant.objects.all()
    participant_list = [{"name": p.name,
                         "link": p.get_absolute_url()
    } for p in participants]

    return {"participants": participant_list}

def navigation_context():
    context = {'participants':{},
               'taxonomy':{},
               'confabulation':{}}
    participant_types = ParticipantTypes.choices()
    for pt in participant_types:
        pt_name = pt[0]
        plist = Participant.objects.filter(participation_group=pt_name)
        p_by_type = [{"name": p.name, "link": p.get_absolute_url()} for p in plist]
        context['participants'][pt_name] = p_by_type

    taxonomy_types = AnalysisType.objects.all()
    for t in taxonomy_types:
        ap_list = AnalysisPoint.objects.filter(analysis_type_id=t.id)

        ap_list_by_type = [{"name": ap.name,
                           "link": ap.get_absolute_url()} for ap in ap_list]
        context['taxonomy'][t.name] = ap_list_by_type

    confab_type = AnalysisType.objects.get(name='Confabulation')
    confab_points = AnalysisPoint.objects.filter(analysis_type_id=confab_type.id)
    confabulation_points = [{"name": ap.name, 'link': ap.get_absolute_url()} for ap in confab_points]
    context['confabulation'] = confabulation_points

    return context

def extend_context(context):
    context['sidebar'] = sidebar_context()
    context['navigation'] = navigation_context()
    return context

def participants(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    participant_list = Participant.objects.all()
    context = {'participant_list':participant_list}
    return render(request, 'confabulation/participants.html', context)

def stories(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    story_list = Story.objects.all().order_by('name')
    context = {'story_list': story_list}
    context['sidebar'] = sidebar_context()
    return render(request, 'confabulation/stories.html', context)

#todo
#def analysisPoints(request)
#    pass


def participant_view(request, participant_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    participant = Participant.objects.get(pk=participant_id)
    participant_stories = Story.objects.filter(participant__id=participant_id).order_by('name')
    context = {'participant':participant, 'stories': participant_stories}
    context['sidebar'] = sidebar_context()
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
    context['sidebar'] = sidebar_context()
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

    context['sidebar'] = sidebar_context()
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

    context['sidebar'] = sidebar_context()
    return render(request, 'confabulation/videoView.html', context)

def era_view(request, era_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    era = Era.objects.get(pk=era_id)
    context = {
        'era': era
    }
    context['sidebar'] = sidebar_context()
    return render(request, 'confabulation/eraView.html', context)

def analysis_view(request, ap_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    ap = AnalysisPoint.objects.get(pk=ap_id)

    context = {
        'analysis_point': ap
    }

    context['sidebar'] = sidebar_context()
    return render(request, 'confabulation/analysisView.html', context)

def analysis_type_view(request, ap_type_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    ap_type = AnalysisType.objects.get(pk=ap_type_id)

    aps = AnalysisPoint.objects.filter(analysis_type_id=ap_type_id).order_by('name')

    context = {
        'analysis_type': ap_type,
        'analysis_points': aps
    }

    context['sidebar'] = sidebar_context()
    return render(request, 'confabulation/analysisTypeView.html', context)

def menumap(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    context={}
    extend_context(context)
    return render(request, 'menumap.html', context)
