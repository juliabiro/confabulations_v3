from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from ..models import  Story, Era, AnalysisPoint, Participant, Keyword, StoryToStoryConnection, Theme
# from ..utils.s3_helpers import *
from ..utils.media_helpers import get_image_url, get_graph_url
from ..utils.connection_helpers import ParticipantConnectionBuilder
from .context_helpers import setup_page_context
from ..utils.story_sorter import sort_story_list
from ..utils.connection_helpers import ConnectionBuilder
from ..utils.graph_scripts import *

def setup_legend(context):
    context['legend']={
        'chain': get_image_url('confabulations/graphs/chain.png', 60),
        'theme': get_image_url('confabulations/graphs/theme.png', 40),
        'story': get_image_url('confabulations/graphs/story.png', 30),
        'inter': get_image_url('confabulations/graphs/inter.png', 40)}

def graph_participant_view(request, participant_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    participant=get_object_or_404(Participant, pk=participant_id)


    node_list, edge_list, groups = collect_participant_chains_themes_stories(participant)
    # node_list, edge_list, groups = legend(participant)

    context = {
        'name': sanitize_name(participant.name),
        'nodes': data_to_script(node_list),
        'edges': data_to_script(edge_list),
        'groups': data_to_script(groups),
    }

    setup_legend(context)
    setup_page_context(context)
    return render(request, 'confabulation/participantGraph.html', context)

def graph_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    static = request.GET.get('static')

    context={}
    if static:
        context={'static': True, 'big_graph_url': get_image_url('confabulations/graphs/big_graph3.jpg', size=4000)}
    else:
        nodes=[]
        edges=[]
        groups=[]
        participants= Participant.objects.distinct()
        for participant in participants:
            n, e, g = collect_participant_chains_themes_stories(participant)
            nodes.extend(n)
            edges.extend(e)
            groups.extend(g)
            groups.append(story_group(participant))


        context['nodes'] = data_to_script(nodes)
        context['edges'] = data_to_script(edges)
        context['groups'] = data_to_script(groups)

    setup_legend(context)
    setup_page_context(context)
    return render(request, 'confabulation/graphView.html', context)

