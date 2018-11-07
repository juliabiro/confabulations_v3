from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Participant, Story, Chain, Theme
from ..utils.s3_helpers import *
from ..utils. media_helpers import get_story_thumb
from ..utils. connection_helpers import get_themes_for_stories, get_chains_for_themes
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

    themes = get_themes_for_stories(participant_stories, participant_id)
    chains = get_chains_for_themes(themes, participant_id)


    context = {'participant':participant, 'stories': participant_stories, 'themes': themes, 'chains': chains}
    setup_page_context(context)
    return render(request, 'confabulation/participantView.html', context)
