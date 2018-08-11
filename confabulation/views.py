from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import redirect
from .models import Participant, Story, Era

def gets3():
    import boto3

    # Get the service client.

    s3_client = boto3.client('s3')
    return s3_client

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    return render(request, 'frontpage.html')

def participants(request):
    participant_list = Participant.objects.all()
    response = ','.join([p.name for p in participant_list])
    context = {'participant_list':participant_list}
    return render(request, 'confabulation/participants.html', context)

def stories(request):
    story_list = Story.objects.all()
    response = ','.join([p.name for p in story_list])
    context = {'story_list':story_list}
    return render(request, 'confabulation/stories.html', context)

def analysisPoints(request):
    pass


def participant_view(request, participant_id):
    participant = Participant.objects.get(pk=participant_id)
    stories = Story.objects.filter(participant__id=participant_id)
    context = {'participant':participant, 'stories': stories}
    return render(request, 'confabulation/participantView.html', context)


def _get_key_from_url(url):
    return url.split("confabulations/")[-1]

def _get_signed_url(key, raise_error = True):
    try:
        s3_client = gets3()

        # this will raise an error if the key doesnt exists
        s3_client.head_object(Bucket='confabulations', Key=key)

        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'confabulations',
                'Key': key
            }
        )

        return url
    except Exception as e:
        if raise_error:
            raise e
        else:
            print (e)
            return None

## there is no ssearch on the html, so all necessary data needs to be here
def storyView(request, story_id):
    story = Story.objects.get(pk=story_id)
    participant = Participant.objects.get(pk=story.participant.id)
    analysis = story.analysis.all()
    video_url = story.video_url
    photos = list(map(lambda p: {"name": p.name, "url": _get_signed_url(_get_key_from_url(p.file_url), raise_error = False )}, story.photos.all()))

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
            url = _get_signed_url(_get_key_from_url(video_url))
            if url:
                context['video_url'] = url

        except Exception as e:
            context["video_error_message"] = "The video at " + video_url + " doesnt exists"

        return render(request, 'confabulation/storyView.html', context)

def thumbnails(request):
    s3 = gets3()
    prefix= 'SG/pilot/thumbs'
    response = s3_client.list_objects(Bucket='confabulations',Prefix=prefix)

    # Generate the URL to get 'key-name' from 'bucket-name'

    thumblist = []

    for c in response['Contents'][1:]:
        key = c['Key']
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'confabulations',
                'Key': key
            }
        )

        name = key.replace(prefix+'/', '').replace('\n','')
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
    s3_client = gets3()
    prefix= 'SG/pilot/SG_360'
    response = s3_client.list_objects(Bucket='confabulations',Prefix=prefix)

    videolist=[]
    for content in response['Contents'][1:]:
        key = content['Key']
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'confabulations',
                'Key': key
            }
        )

        videolist.append({
            'name': key.replace(prefix+'/', ""),
            'url': url
        })

        context = {
            'videos_list':videolist
        }

    return render(request, 'confabulation/videos.html', context)

def video_view(request, video_name):
    s3_client = gets3()
    prefix= 'SG/pilot/SG_360'
    key = prefix+'/'+video_name

    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'confabulations',
            'Key': key+".mp4"
        }
    )

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
