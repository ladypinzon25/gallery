# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-29 20:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_auto_20180826_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gallery.Categoria'),
        ),
    ]