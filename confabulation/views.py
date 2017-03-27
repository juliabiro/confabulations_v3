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



