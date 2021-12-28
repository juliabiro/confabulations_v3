"""dbbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.conf.urls import re_path
from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500
from confabulation.views.error_views import error_404, error_500

login_context={
    'is_login' : True
}
if 'LOCAL' in os.environ:
    login_context['site_name'] = "LOCAL login"
else:
    login_context['site_name'] = "Beyond The Photograph"

urlpatterns = [
    re_path(r'^login/$', auth_views.LoginView.as_view(extra_context=login_context), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^confabulation/', include ('confabulation.urls')),
    re_path(r'^', include('confabulation.urls')),
]

handler404 = error_404
handler500 = error_500
