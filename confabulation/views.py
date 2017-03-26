from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import redirect

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    return render(request, 'frontpage.html')



