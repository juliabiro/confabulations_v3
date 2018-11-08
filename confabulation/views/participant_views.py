from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Participant, Story, Chain, Theme, ConnectionRange
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

    themes_with_stories_intra = get_themes_for_stories(participant_id, connection_type="Intraconnection")

    themes_with_stories_inter = get_themes_for_stories(participant_id, connection_type="Interconnection")

    context = {'participant':participant, 'stories': participant_stories, 'themes_with_stories_intra': themes_with_stories_intra, 'themes_with_stories_inter': themes_with_stories_inter}
    setup_page_context(context)
    return render(request, 'confabulation/participantView.html', context)
