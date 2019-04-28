from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from ..models import  Story, Era, AnalysisPoint, Participant, Keyword, StoryToStoryConnection, Theme
from ..utils.s3_helpers import *
from ..utils.connection_helpers import ParticipantConnectionBuilder
from .context_helpers import setup_page_context
from ..utils.story_sorter import sort_story_list
from ..utils.connection_helpers import ConnectionBuilder
from ..utils.graph_scripts import participant_story_connections



def graph_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    context={
        'participant_graphs':[]
    }
    for participant in Participant.objects.distinct():
        node_list, edge_list, group = participant_story_connections(participant)

        context['participant_graphs'].append({
            'name': participant.name.replace(' ','_'),
            'nodes': node_list,
            'edges': edge_list,
            'group': group
        })


    setup_page_context(context)
    return render(request, 'confabulation/graphView.html', context)

