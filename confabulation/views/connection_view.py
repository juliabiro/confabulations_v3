from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Connection
from ..utils.s3_helpers import *
from ..utils.connection_helpers import ConnectionBuilder
from .context_helpers import setup_page_context

def connection_view(request, connection_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    connection = Connection.objects.get(pk=connection_id)

    context = {
        'connection': connection
    }

    connectionBuilder = ConnectionBuilder(connection.connection_range)
    themes = connectionBuilder.buildthemes()
    chains = connectionBuilder.buildchains()
    context['themes'] = themes
    context['chains'] = chains
    setup_page_context(context)
    return render(request, 'confabulation/connectionView.html', context)

