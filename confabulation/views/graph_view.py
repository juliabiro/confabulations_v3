from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from ..models import  Story, Era, AnalysisPoint, Participant, Keyword, StoryToStoryConnection, Theme
from ..utils.s3_helpers import *
from ..utils.connection_helpers import ParticipantConnectionBuilder
from .context_helpers import setup_page_context
from ..utils.story_sorter import sort_story_list
from ..utils.connection_helpers import ConnectionBuilder

def graph_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    story_list = sort_story_list(list(Story.objects.distinct()))
    connections = ConnectionBuilder('Intraconnection').buildstoryconnections()

    context = {'story_list': story_list, 'connections':connections}

    setup_page_context(context)
    return render(request, 'confabulation/graphView.html', context)

