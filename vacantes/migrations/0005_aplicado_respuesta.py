# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-06 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacantes', '0004_auto_20170306_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='aplicado',
            name='respuesta',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
