# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 12:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacantes', '0010_pregunta_provincia'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pregunta',
            new_name='Preguntado',
        ),
    ]
