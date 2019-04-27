from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from ..models import  Story, Era, AnalysisPoint, Participant, Keyword, StoryToStoryConnection, Theme
from ..utils.s3_helpers import *
from ..utils.connection_helpers import ParticipantConnectionBuilder
from .context_helpers import setup_page_context
from ..utils.story_sorter import sort_story_list
from ..utils.connection_helpers import ConnectionBuilder

COLORS ={'4':'red','5':'green', '7':'blue', '8':'olive', '9':'purple', '10':'lime', '11':'teal', '3':'gray'}
def _get_color(s):
    participant_id = s.participant.id

    return COLORS[str(participant_id)]

def graph_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


    connections = ConnectionBuilder('Intraconnection').buildstoryconnections()

    stories = []
    for c in connections:
        stories.append(c.story1)
        stories.append(c.story2)

    nodes = [{'id': s.id,
              'label':s.name,
              'color': _get_color(s),
              'url': s.get_absolute_url()}
             for s in list(set(stories))]
    edges =[{'node1': {'id': c.story1.id},
             'node2': {'id': c.story2.id}}
            for c in connections]
    context = {'node_list':nodes, 'edges':edges}

    setup_page_context(context)
    return render(request, 'confabulation/graphView.html', context)

