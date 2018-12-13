from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from ..models import Story, AnalysisPoint, AnalysisType
from ..utils.s3_helpers import *
from .context_helpers import setup_page_context

def analysis_view(request, ap_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    ap = AnalysisPoint.objects.get(pk=ap_id)

    context = {
        'analysis_point': ap
    }
    stories = list(Story.objects.filter(analysis__id=ap.id).distinct().order_by('name'))
    context['stories'] = stories

    setup_page_context(context)
    return render(request, 'confabulation/analysisView.html', context)

def analysis_type_view(request, ap_type_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    ap_type = AnalysisType.objects.get(pk=ap_type_id)

    aps = AnalysisPoint.objects.filter(analysis_type_id=ap_type_id).order_by('name')
    context = {
        'analysis_type': ap_type,
        'analysis_points': [{'name': ap.name,
                             'color_code': ap.color_code,
                             'url': ap.get_absolute_url } for ap in aps]
    }

    setup_page_context(context)
    return render(request, 'confabulation/analysisTypeView.html', context)

