from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from .context_helpers import setup_page_context
from ..models import AnalysisPoint
from ..utils.s3_helpers import get_signed_video_url
from ..utils.data import TAXONOMY_VIDEO_KEY

# Create your views here.
def index(request):
    video_url = TAXONOMY_VIDEO_KEY
    url = get_signed_video_url(video_url)
    context = {}
    context['video_url'] = url

    try:
        confabulation = AnalysisPoint.objects.filter(name="Confabulation")[0]
        context['confabulation_url'] = confabulation.get_absolute_url()
        going_beyond=AnalysisPoint.objects.filter(name="Going Beyond")[0]
        context['going_beyond_url'] = going_beyond.get_absolute_url()

    except Exception as e:
        print(e)

    setup_page_context(context, navbar=False)
    return render(request, 'frontpage.html', context)

def about(request):
    context = setup_page_context(None, navbar=False)
    return render(request, 'confabulation/about.html', context)

def author(request):
    context = setup_page_context(None, navbar=False)
    return render(request, 'confabulation/author.html', context)

def menumap(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    context = setup_page_context(None, navbar=True)
    return render(request, 'menumap.html', context)
