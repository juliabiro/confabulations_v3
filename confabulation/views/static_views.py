from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect

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
    context={}
    extend_context(context)
    return render(request, 'menumap.html', context)
