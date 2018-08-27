# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gallery.models import Media
from gallery.models import User
from django.http import HttpResponse, JsonResponse
from django.core import serializers as jsonserializer
from django.http import Http404

def all_media(request):
    all_media_objects = Media.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_media_objects))


def all_users(request):
    all_users_objects = User.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_users_objects))

def user_by_id(request, user_id):
    try:
        user = User.objects.filter(idUser=user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist.")
    return HttpResponse(jsonserializer.serialize("json", user))
