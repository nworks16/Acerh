# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-06 18:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacantes', '0005_aplicado_respuesta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aplicado',
            name='respuesta',
            field=models.TextField(blank=True),
        ),
    ]
