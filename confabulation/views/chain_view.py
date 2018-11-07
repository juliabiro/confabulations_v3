from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Story, Chain, Theme
from ..utils.connection_helpers import get_themes_for_stories, get_chains_for_themes
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

    chain = Chain.objects.get(pk=chain_id)

    themes = chain.themes.all()

    context = {'chain':chain, 'themes': themes}
    setup_page_context(context)
    return render(request, 'confabulation/chainView.html', context)
