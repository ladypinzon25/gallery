# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gallery.models import Media, Clip
from gallery.models import User
from gallery.models import Categoria
from django.http import HttpResponse, JsonResponse
from django.core import serializers as jsonserializer
from django.views.decorators.csrf import  csrf_exempt
from django.core.mail import send_mail
import json
import logging
from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

logger = logging.getLogger(__name__)

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
        data = json.loads(request.body)
        name = data["name"]
        lastName = data["lastName"]
        email = data["email"]
        country = data["country"]
        city = data["city"]
        pws = data["password"]
        id = data["idUser"]
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
            data=json.loads(request.body)
            name = data["name"]
            lastName = data["lastName"]
            email = data["email"]
            country = data["country"]
            city = data["city"]
            pws = data["password"]
            id = data["idUser"]
            _user = User(name = name,lastName=lastName,email=email,country=country,city=city,password=pws,idUser=id)
            try:
                _user.save()
                res = {"status": "Ok", "Content:": "Usuario creado"}
            except:

                res = {"status": "Error", "Content:": "Error al crear usuario"}

            return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            return HttpResponse('Metodo no definido')


def user_by_id(request, user_id):
    try:
        user = User.objects.filter(idUser=user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist.")
    return HttpResponse(jsonserializer.serialize("json", user))


def all_categories (request):
    return HttpResponse(jsonserializer.serialize("json", Categoria.objects.all()))


def media_by_categoria (request, categoria_id):
    mediaList = Media.objects.filter(categoria=categoria_id)
    return HttpResponse(jsonserializer.serialize("json", mediaList))


#Crear clip
#http://localhost:8000/api/v1/gallery/create_clip/
# {
# 	"idClip":1,
# 	"name":"momento de prueba",
# 	"start":5,
# 	"end":16,
# 	"idMedia":1
# }
#   Si se le pasa un id que ya existe lo sobreescribe!!!


@csrf_exempt
def create_clip(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_clip = Clip.objects.latest("idClip").idClip +1
        name_clip = data["name"]
        seg_init = data["start"]
        seg_end = data["end"]
        user_clip = User.objects.get(idUser=data["idUser"])
        user_name = user_clip.name
        media_clip = Media.objects.get(idMedia=data["idMedia"])
        user_media = media_clip.user
        new_clip = Clip(idClip=id_clip, name=name_clip, seg_initial=seg_init, seg_final=seg_end, user=user_clip, media=media_clip)
        logging.error('datos obtenidos')
        try:
            new_clip.save()
            logging.error('guardando')
            send_mail('Nuevo Clip',
                      'Saludos desde Clipstar, el usuario '+ user_clip.name +' '+ user_clip.lastName +
                      ' ha creado un nuevo clip en el video de '+ user_media.name +' ' + user_media.lastName+'.',
                      'clipstaragil6@gmail.com',
                      [user_clip.email,user_media.email],
                      fail_silently=False)
            res = {"status": "Ok", "Content:": "Clip creado"}
        except:
            res = {"status": "Error", "Content:": "Error al crear clip"}


        return HttpResponse(json.dumps(res), content_type="application/json")
    else:
        return HttpResponse('Metodo no definido')

#Retorna la infromacion de un clip dado un id
#http://localhost:8000/api/v1/gallery/clip/<ID_CLIP>/
def clip_by_id(request, clip_id):
    try:
        clip = Clip.objects.filter(idClip=clip_id)
    except Clip.DoesNotExist:
        raise Http404("User does not exist.")
    return HttpResponse(jsonserializer.serialize("json", clip))


#Retorna todos los clips pertenecientes a un id de Media
def all_clips_by_media(request,media_id):
    try:
        media = Media.objects.get(idMedia=media_id)
        list = Clip.objects.filter(media=media)
    except Media.DoesNotExist:
        raise Http404("Clips not found")
    return HttpResponse(jsonserializer.serialize("json", list))

@csrf_exempt
def simple_upload(request,id_user):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        try:
            _user = User.objects.get(idUser=id_user)
            _user.image = uploaded_file_url
            _user.save()
        except:
            res = {"status": "Error", "Content:": "Error al crear clip"}
            return HttpResponse(json.dumps(res), content_type="application/json")
        return HttpResponse(jsonserializer.serialize("json",_user))
    else:
        return HttpResponse('Metodo no definido')
