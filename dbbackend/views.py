from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    next = request.GET('next')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(next) 
    else:
        return HttpResponse("Invalid login, try again")
