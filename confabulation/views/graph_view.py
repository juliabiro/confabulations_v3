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

    context={
        'participant_graphs':[],
    }
    participant=get_object_or_404(Participant, pk=participant_id)


    #node_list, edge_list, group = participant_story_connections(participant)
    # instead get the whole package:

    node_list, edge_list, groups = participant_chains_themes_stories(participant)

    context['participant_graphs'].append({
        'name': participant.name.replace(' ','_'),
        'nodes': node_list,
        'edges': edge_list,
        'groups': groups,
    })

    setup_page_context(context)
    return render(request, 'confabulation/participantGraph.html', context)

def graph_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    context={
        'participant_graphs':[],
        'story_to_participant_graph':{
            'nodes':"",
            'edges':"",
        }
    }
    participants= Participant.objects.distinct()
    for participant in participants:
        node_list, edge_list, group = participant_story_connections(participant)


        context['participant_graphs'].append({
            'name': participant.name.replace(' ','_'),
            'nodes': node_list,
            'edges': edge_list,
            'groups': ','.join([group, story_group(participant)])
        })

    context['story_to_participant_graph']['nodes']=','.join([participant_node(p) for p in participants])
    context['story_to_participant_graph']['edges']=','.join([story_to_participant_edges(p) for p in participants])

    setup_page_context(context)
    return render(request, 'confabulation/graphView.html', context)

