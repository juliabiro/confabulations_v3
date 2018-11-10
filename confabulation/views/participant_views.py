from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Participant, Story, Chain, Theme, ConnectionRange
from ..utils.s3_helpers import *
from ..utils. media_helpers import get_story_thumb
from ..utils. connection_helpers import ChainsThemesStories
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
    context = {'participant':participant}

    intrachains = ChainsThemesStories().buildchains(participant_id, 'Intraconnection')
    interchains = ChainsThemesStories().buildchains(participant_id, 'Interconnection')

    chainless_themes = ChainsThemesStories().buildthemes(participant_id, 'Intraconnection')
    story_connections_intra = ChainsThemesStories().buildstoryconnections(participant_id, "Intraconnection")
    story_connections_inter = ChainsThemesStories().buildstoryconnections(participant_id, "Interconnection")

    if interchains:
        context['interconnections'] = interchains
    if intrachains:
        context['intraconnections'] = intrachains
    if chainless_themes:
        context['chainless_themes'] = chainless_themes

    if story_connections_intra:
        context['story_connections_intra'] = story_connections_intra
    if story_connections_inter:
        context['story_connections_inter'] = story_connections_inter

    setup_page_context(context)
    return render(request, 'confabulation/participantView.html', context)
