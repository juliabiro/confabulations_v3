from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Participant, Story, Chain, Theme, ConnectionRange
from ..utils.s3_helpers import *
from ..utils. media_helpers import *
from ..utils. connection_helpers import buildchains, buildthemes, buildstoryconnections, buildsinglestories
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

    p_stories = Story.objects.get(participant_id=participant_id)
    # story_thumbs=[]
    # for s in p_stories:
    #     story_thumb=get_cloudinary_image_thumb(s.name)
    #     story_thumb.append({
    #         'name' : s.name,
    #         'id': 'story/'+s.id,
    #         'thumb': story_thumb
    #     })
    # context['thumbs'] = story_thumbs
    intrachains = buildchains(participant_id, 'Intraconnection')
    interchains = buildchains(participant_id, 'Interconnection')

    chainless_themes = buildthemes(participant_id, 'Intraconnection')
    story_connections_intra = buildstoryconnections(participant_id, "Intraconnection")
    story_connections_inter = buildstoryconnections(participant_id, "Interconnection")

    single_stories = buildsinglestories(participant_id)

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

    if single_stories:
        context['single_stories'] = single_stories

    setup_page_context(context)
    return render(request, 'confabulation/participantView.html', context)
