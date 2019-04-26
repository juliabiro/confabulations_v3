from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Participant, Story, Theme, Chain, AnalysisPoint, AnalysisType
from .context_helpers import setup_page_context
from ..forms import SearchForm

import re

def search_list_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    search = SearchForm(request.GET)['search'].value()

    m=re.search('\d+', search)
    if m:
        prefix = search[0:m.start()].strip()
        postfix = int(m.group())

        stories = Story.objects.filter(name__icontains=prefix).filter(name__icontains=postfix)
    else:
        stories = Story.objects.filter(name__icontains=search)

    participants = Participant.objects.filter(name__icontains=search)
    themes = Theme.objects.filter(name__icontains=search)
    chains = Chain.objects.filter(name__icontains=search)
    aps = AnalysisPoint.objects.filter(name__icontains=search)
    ap_types = AnalysisType.objects.filter(name__icontains=search)

    context = {}
    if stories:
        context['stories'] = [{'name':s.name, 'url': s.get_absolute_url()} for s in stories]
    if participants:
        context['participants'] = [{'name':s.name, 'url': s.get_absolute_url()} for s in participants]
    if themes:
        context['themes'] = [{'name':s.name, 'url': s.get_absolute_url()} for s in themes]
    if chains:
        context['chains'] = [{'name':s.name, 'url': s.get_absolute_url()} for s in chains]
    if aps:
        context['aps'] = [{'name':s.name, 'url': s.get_absolute_url()} for s in aps]
    if ap_types:
        context['ap_types'] = [{'name':s.name, 'url': s.get_absolute_url()} for s in ap_types]

    if len(context) is 0:
        context['nohits'] = True
    context['search'] = search
    setup_page_context(context,
                       sidebar_right=False,
                       sidebar_left=True)
    return render(request, 'confabulation/searchView.html', context)
