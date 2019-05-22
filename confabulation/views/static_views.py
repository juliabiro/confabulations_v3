from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from .context_helpers import setup_page_context
from ..models import Participant
from ..utils.media_helpers import get_graph_url

# Create your views here.
def index(request):
    context = {}
    context['participants']=[]
    context['big_graph_url']= get_graph_url(size=800, opacity=30)

    plist=list(Participant.objects.distinct())
    if len(plist)>0:
        for p in plist[0:-1]:
            context['participants'].append({'name': p.name, 'url':p.get_absolute_url()})
        if len(plist)>1:
            context['last'] = {'name': plist[-1].name, 'url': plist[-1].get_absolute_url()}

    setup_page_context(context, sidebar_left=True)
    return render(request, 'frontpage.html', context)

def menumap(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    context = setup_page_context(None, navbar=True)
    return render(request, 'menumap.html', context)
