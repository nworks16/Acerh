# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-17 06:22
from __future__ import unicode_literals

from django.db import migrations, models
import vacantes.models


class Migration(migrations.Migration):

    dependencies = [
        ('vacantes', '0002_auto_20170124_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='aplicado',
            name='entrevista',
            field=models.FileField(blank=True, upload_to=vacantes.models.upload_location),
        ),
    ]
