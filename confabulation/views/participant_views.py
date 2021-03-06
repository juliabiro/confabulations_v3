from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from ..models import Participant, Story
from ..utils. connection_helpers import ParticipantConnectionBuilder
from .context_helpers import setup_page_context
from ..utils.story_sorter import sort_story_list

def participants(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    participant_list = [{'name': p.name, 'url': p.get_absolute_url()} for p in Participant.objects.all()]
    context = {'participant_list':participant_list}
    setup_page_context(context)
    return render(request, 'confabulation/participants.html', context)

def participant_view(request, participant_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    participant = get_object_or_404(Participant, pk=participant_id)
    context = {'participant':participant}

    intraBuilder = ParticipantConnectionBuilder(participant_id, 'Intraconnection')
    interBuilder = ParticipantConnectionBuilder(participant_id, 'Interconnection')

    p_stories = Story.objects.filter(participant_id=participant_id).order_by('name')
    p_stories_sorted = sort_story_list(list(p_stories))

    context["participant_stories"] = p_stories_sorted

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
