# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from gallery.models import Media

from gallery.models import User
from .models import Clip,Categoria


#admin.site.register(Media)
#admin.site.register(User)


class UserAdmin (admin.ModelAdmin):
    list_display = ['idUser','name','lastName']

class MediaAdmin (admin.ModelAdmin):
    list_display = ['idMedia','mediaType','title','user','fec_create','categoria']

class CategoriaAdmin (admin.ModelAdmin):
    list_display = ['idCategoria', 'name']

class ClipAdmin (admin.ModelAdmin):
    list_display = ['idClip', 'name','seg_initial','seg_final']

admin.site.register(User,UserAdmin)
admin.site.register(Media,MediaAdmin)
admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Clip,ClipAdmin)


