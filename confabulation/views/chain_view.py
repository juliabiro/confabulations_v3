from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from ..models import Story, Chain, Theme
from .context_helpers import setup_page_context

def chains(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    chain_list = Chain.objects.all()
    context = {'chain_list':chain_list}
    setup_page_context(context)
    return render(request, 'confabulation/chains.html', context)

def chain_view(request, chain_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    chain = get_object_or_404(Chain, pk=chain_id)

    themes = chain.themes.all()

    connection_range = 'Intra-connection' if chain.connection_range == "Intraconnection" else 'Inter-connection'

    context = {'chain':chain, 'themes': themes, 'connection_range': connection_range}
    setup_page_context(context)
    return render(request, 'confabulation/chainView.html', context)
