from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    template = loader.get_template('administration/index.html')
    return HttpResponse(template.render(request=request))

def connect_admin_space(request):
    template = loader.get_template('administration/admin_connect_space.html')
    return HttpResponse(template.render(request=request))

def update_profile_interface(request):
    template = loader.get_template('administration/update_profile.html')
    return HttpResponse(template.render(request=request))

def administration_interface(request):
    template = loader.get_template('administration/administration_interface.html')
    return HttpResponse(template.render(request=request))
