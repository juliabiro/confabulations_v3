from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Participant, Story
from ..utils. connection_helpers import ParticipantConnectionBuilder
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

    intraBuilder = ParticipantConnectionBuilder(participant_id, 'Intraconnection')
    interBuilder = ParticipantConnectionBuilder(participant_id, 'Interconnection')

    p_stories = Story.objects.filter(participant_id=participant_id).order_by('name')
    context["participant_stories"] = p_stories

    story_connections_intra = intraBuilder.buildstoryconnections()
    story_connections_inter = interBuilder.buildstoryconnections()

    if story_connections_intra:
        context['story_connections_intra'] = story_connections_intra
    if story_connections_inter:
        context['story_connections_inter'] = story_connections_inter

    setup_page_context(context,
                       sidebar_right=True,
                       sidebar_left=True,
                       participant_id=participant_id)
    return render(request, 'confabulation/participantView.html', context)
