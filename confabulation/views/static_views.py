from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from .context_helpers import setup_page_context
from ..utils.s3_helpers import get_signed_video_url, parse_key_from_url
from ..utils.data import TAXONOMY_VIDEO_KEY

# Create your views here.
def index(request):
    video_url = TAXONOMY_VIDEO_KEY
    url = get_signed_video_url(parse_key_from_url(video_url))
    context = {}
    context['video_url'] = url
    return render(request, 'frontpage.html', context)

def about(request):
    return render(request, 'about.html')

def author(request):
    return render(request, 'author.html')

def menumap(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    setup_page_context(None, navbar=False)
    return render(request, 'menumap.html', context)
