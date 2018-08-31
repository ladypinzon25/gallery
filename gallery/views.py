# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gallery.models import Media, Clip
from gallery.models import User
from gallery.models import Categoria
from django.http import HttpResponse, JsonResponse
from django.core import serializers as jsonserializer
from django.views.decorators.csrf import  csrf_exempt
import json
import logging
from django.http import Http404

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
        id_clip = data["idClip"]
        name_clip = data["name"]
        seg_init = data["start"]
        seg_end = data["end"]
        parent_id = data["idMedia"]
        new_clip = Clip(idClip=id_clip, name=name_clip, seg_initial=seg_init, seg_final=seg_end)
        logging.error('datos obtenidos')
        try:
            new_clip.save()
            logging.error('guardando')
            Media.add_clip(Media.objects.get(idMedia=parent_id), new_clip, parent_id)
            logging.error('agregando')
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
       list = Media.objects.get(idMedia=media_id).clips.all()
    except Media.DoesNotExist:
        raise Http404("Clips not found")
    return HttpResponse(jsonserializer.serialize("json", list))