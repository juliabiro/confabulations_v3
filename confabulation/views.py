from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponse("Hello, World! This is Bozsis TOP SECRET confabulations site")

    else:
        return defaultcontent()

def defaultcontent(request):
        return HttpResponse("Hello, World! This is Bozsis confabulation site")

