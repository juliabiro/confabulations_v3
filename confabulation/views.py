from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import redirect
from models import Participant, Story, AnalysisPoint

def gets3():
    import boto3

    # Get the service client.

    s3 = boto3.client('s3')#, config=Config(signature_version='s3v4'))
    return s3

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


def participantView(request, participant_id):
    participant = Participant.objects.get(pk=participant_id)
    stories = Story.objects.filter(participant__id=participant_id)
    context = {'participant':participant, 'stories': stories}
    return render(request, 'confabulation/participantView.html', context)


## there is no ssearch on the html, so all necessary data needs to be here
def storyView(request, story_id):
    story = Story.objects.get(pk=story_id)
    participant = Participant.objects.get(pk=story.participant.id)
    analysis = story.analysis.all()

    video_url = story.video_url
    url = ""
    if video_url:
        key = video_url[video_url.find('confabulations'):]

        s3 = gets3()
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'confabulations',
                'Key': key
            }
        )


    context = {'story': story,
               'participant':{
                   'name': participant.name,
                   'id': participant.id
               },
               'analysis':analysis,
    }

    if url:
        context['video_url'] = url
    print context
    return render(request, 'confabulation/storyView.html', context)

def thumbnails(request):
    s3 = gets3()
    prefix= 'SG/pilot/thumbs'
    response = s3.list_objects(Bucket='confabulations',Prefix=prefix)

    # Generate the URL to get 'key-name' from 'bucket-name'

    thumblist = []

    for c in response['Contents'][1:]:
        key = c['Key']
        url = s3.generate_presigned_url(
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
    s3 = gets3()
    prefix= 'SG/pilot/SG_360'
    response = s3.list_objects(Bucket='confabulations',Prefix=prefix)

    videolist=[]
    for c in response['Contents'][1:]:
        key = c['Key']
        url = s3.generate_presigned_url(
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

def videoView(request, video_name):
    s3 = gets3()
    prefix= 'SG/pilot/SG_360'
    key = prefix+'/'+video_name

    url = s3.generate_presigned_url(
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

    return render(request, 'confabulation/video_view.html', context)
