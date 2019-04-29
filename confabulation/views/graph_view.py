from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from ..models import  Story, Era, AnalysisPoint, Participant, Keyword, StoryToStoryConnection, Theme
from ..utils.s3_helpers import *
from ..utils.connection_helpers import ParticipantConnectionBuilder
from .context_helpers import setup_page_context
from ..utils.story_sorter import sort_story_list
from ..utils.connection_helpers import ConnectionBuilder
from ..utils.graph_scripts import *


def graph_participant_view(request, participant_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    participant=get_object_or_404(Participant, pk=participant_id)


    #node_list, edge_list, group = participant_story_connections(participant)
    # instead get the whole package:

    node_list, edge_list, groups = collect_participant_chains_themes_stories(participant)

    context = {
        'name': sanitize_name(participant.name),
        'nodes': data_to_script(node_list),
        'edges': data_to_script(edge_list),
        'groups': data_to_script(groups),
    }

    setup_page_context(context)
    return render(request, 'confabulation/participantGraph.html', context)

def graph_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


    nodes=[]
    edges=[]
    groups=[]
    participants= Participant.objects.distinct()
    for participant in participants:
        #n, e, g = collect_participant_story_connections(participant)
        n, e, g = collect_participant_chains_themes_stories(participant)
        nodes.extend(n)
        edges.extend(e)
        groups.extend(g)
        #nodes.append(participant_node(participant))
        #edges.extend(collect_story_to_participant_edges(participant))
        groups.append(story_group(participant))

    context={}

    context['nodes'] = data_to_script(nodes)
    context['edges'] = data_to_script(edges)
    context['groups'] = data_to_script(groups)


    setup_page_context(context)
    return render(request, 'confabulation/graphView.html', context)

