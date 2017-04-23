from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import redirect
from models import Participant, Story, AnalysisPoint

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

    context = {'story': story,
               'participant':{
                   'name': participant.name,
                   'id': participant.id
               },
               'analysis':analysis 
    }
    return render(request, 'confabulation/storyView.html', context)

def gets3():
    import boto3

    # Get the service client.

    s3 = boto3.client('s3')#, config=Config(signature_version='s3v4'))
    return s3

def thumbnails(request):
    s3 = gets3()
    # Generate the URL to get 'key-name' from 'bucket-name'
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'confabulations',
            'Key': 'SG/pilot/thumbs/SG01.png'
        }
    )

    # Use the URL to perform the GET operation. You can use any method you like
    # to send the GET, but we will use requests here to keep things simple.
    context = {
        'thumbnail_list':[
            {
                "name":'SG01',
                'url': url
            }
        ]
    }

    return render(request, 'confabulation/thumbnails.html', context)

def videos(request):
    s3 = gets3()
    # Generate the URL to get 'key-name' from 'bucket-name'
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'confabulations',
            'Key': 'SG/pilot/SG360/SG01.mp4'
        }
    )

    # Use the URL to perform the GET operation. You can use any method you like
    # to send the GET, but we will use requests here to keep things simple.
    context = {
        'videos_list':[
            {
                "name":'SG01',
                'url': url
            }
        ]
    }

    return render(request, 'confabulation/videos.html', context)
