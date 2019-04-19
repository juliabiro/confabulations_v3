from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Story, Chain, Theme
from .context_helpers import setup_page_context

def themes(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    theme_list = Theme.objects.all()
    context = {'theme_list':theme_list}
    setup_page_context(context)
    return render(request, 'confabulation/themes.html', context)

def theme_view(request, theme_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    theme = Theme.objects.get(pk=theme_id)

    stories = theme.stories.all()
    chains = Chain.objects.filter(themes__id=theme_id)

    connection_range = "Intra-connection" if theme.connection_range == 'Intraconnection' else "Inter-connection"


    context = {'theme':theme, 'stories': stories, 'chains': chains, 'connection_range': connection_range}

    setup_page_context(context)
    return render(request, 'confabulation/themeView.html', context)
