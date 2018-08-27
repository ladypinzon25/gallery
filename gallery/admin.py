# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from gallery.models import Media

from gallery.models import User
from .models import Clip,Categoria

admin.site.register(Clip)
admin.site.register(Media)
#admin.site.register(User)
admin.site.register(Categoria)

class UserAdmin (admin.ModelAdmin):
    list_display = ['idUser','name','lastName']

admin.site.register(User,UserAdmin)


