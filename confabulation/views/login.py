from django.shortcuts import render
from django.conf import settings
from .context_helpers import setup_page_context

def user_login(request):
    context={}
    setup_page_context(context)
    return render (request, 'registration/login.html', context)
