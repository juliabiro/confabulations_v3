from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from .context_helpers import setup_page_context

# Create your views here.
def index(request):
    return render(request, 'frontpage.html')

def about(request):
    return render(request, 'about.html')

def author(request):
    return render(request, 'author.html')

def menumap(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    setup_page_context(None, navbar=False)
    return render(request, 'menumap.html', context)
