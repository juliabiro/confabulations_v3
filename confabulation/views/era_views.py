from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from ..models import Era
from .context_helpers import setup_page_context

def era_view(request, era_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    era = get_object_or_404(Era, pk=era_id)
    context = {
        'era': era
    }
    setup_page_context(context)
    return render(request, 'confabulation/eraView.html', context)
