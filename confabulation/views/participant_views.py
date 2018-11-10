from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Participant, Story
from ..utils.s3_helpers import *
from ..utils. media_helpers import get_story_thumb
from .context_helpers import setup_page_context

def participants(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    participant_list = Participant.objects.all()
    context = {'participant_list':participant_list}
    setup_page_context(context)
    return render(request, 'confabulation/participants.html', context)

def participant_view(request, participant_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    participant = Participant.objects.get(pk=participant_id)
    participant_stories = Story.objects.filter(participant__id=participant_id).order_by('name')
    context = {'participant':participant, 'stories': participant_stories}
    setup_page_context(context)
    return render(request, 'confabulation/participantView.html', context)
