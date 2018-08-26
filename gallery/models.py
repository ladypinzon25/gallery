# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


import datetime


class Clip(models.Model):
    idClip = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    seg_initial = models.BigIntegerField()
    seg_final = models.BigIntegerField()


class User(models.Model):
    idUser = models.FloatField(primary_key=True)
    name = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=500)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
#photo = models.ImageField(upload_to='/images/')



class Media(models.Model):
    MEDIA_TYPES_CHOICES = (
        ('Video', 'VIDEO'),
        ('Audio', 'AUDIO'),
    )
    idMedia = models.FloatField(primary_key=True)
    mediaType = models.CharField(max_length=10, choices=MEDIA_TYPES_CHOICES, default='Video')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
    clips = models.ManyToManyField(Clip, blank=True)
    fec_create = models.DateField(default=datetime.date.today)


class Categoria(models.Model):
    idCategoria = models.FloatField(primary_key=True)
    name = models.CharField(max_length=255)