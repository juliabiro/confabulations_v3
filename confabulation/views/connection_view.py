from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Connection, Participant, Chain
from ..utils.connection_helpers import ParticipantConnectionBuilder
from .context_helpers import setup_page_context


class ConnectionViewElement():
    def __init__(self, data):
        self.p_id = data['id']
        self.name = data['name']
        self.chains = data['chains']
        self.themes = data['themes']
        self.storyconnections = data ['storyconnections']

def connection_view(request, connection_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    connection = Connection.objects.get(pk=connection_id)

    participants = Participant.objects.distinct()

    context = {
        'connection': connection,
        'participants': []
    }

    inter_chain = None
    if connection.connection_range == "Interconnection":
        inter_chain=Chain.objects.filter(connection_range='Interconnection').distinct()
        if len(inter_chain) is 1:
            context['inter_chain'] = inter_chain[0]

    for p in participants:
        builder = ParticipantConnectionBuilder(p.id, connection.connection_range)
        chains = builder.buildchains()
        themes = builder.buildthemes()
        s2s = builder.buildstoryconnections()

        context['participants'].append(
            ConnectionViewElement({'name': p.name,
                                   'id': p.id,
                                   'chains': chains,
                                   'themes': themes,
                                   'storyconnections': s2s

            })
        )


    setup_page_context(context)
    return render(request, 'confabulation/connectionView.html', context)

