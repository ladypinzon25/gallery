# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gallery.models import Media
from gallery.models import User
from django.http import HttpResponse, JsonResponse
from django.core import serializers as jsonserializer
from django.views.decorators.csrf import  csrf_exempt
import json

def all_media(request):
    all_media_objects = Media.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_media_objects))


def all_users(request):
    all_users_objects = User.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_users_objects))

#Se define endpoint para actualizacion de datos de usuario
@csrf_exempt
def modify(request):

    if request.method == 'POST':

        name = request.POST.get('name', None)
        lastName = request.POST.get('lastName', None)
        email = request.POST.get('email', None)
        country = request.POST.get('country', None)
        city = request.POST.get('city', None)
        pws = request.POST.get('password', None)
        id = request.POST.get('idUser', None)
        _user=User()
        if(_user.update(id, name, lastName,email,country,city,pws)):
            res={"status":"Ok","Content:":"Usuario Modificado"}
        else:
            res={"status":"Error","Content:":"Error al modificar usuario"}

        return HttpResponse(json.dumps(res),content_type="application/json")
    else:
        return  HttpResponse('Metodo no definido')

#Se define endpoint para creacion de usuario
@csrf_exempt
def create(request):

        if request.method == 'POST':

            name = request.POST.get('name', None)
            lastName = request.POST.get('lastName', None)
            email = request.POST.get('email', None)
            country = request.POST.get('country', None)
            city = request.POST.get('city', None)
            pws = request.POST.get('password', None)
            id = request.POST.get('idUser', None)
            _user = User(name = name,lastName=lastName,email=email,country=country,city=city,password=pws,idUser=id)
            try:
                _user.save()
                res = {"status": "Ok", "Content:": "Usuario creado"}
            except:

                res = {"status": "Error", "Content:": "Error al crear usuario"}

            return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            return HttpResponse('Metodo no definido')
