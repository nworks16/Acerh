# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-27 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacantes', '0012_auto_20170324_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='aplicado',
            name='respuesta2',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='aplicado',
            name='respuesta3',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='aplicado',
            name='respuesta4',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='aplicado',
            name='respuesta5',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='aplicado',
            name='respuesta6',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='aplicado',
            name='respuesta7',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='aplicado',
            name='respuesta8',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='vacante',
            name='pregunta1',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='vacante',
            name='pregunta2',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='vacante',
            name='pregunta3',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='vacante',
            name='pregunta4',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='vacante',
            name='pregunta5',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='vacante',
            name='pregunta6',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='vacante',
            name='pregunta7',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='vacante',
            name='pregunta8',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='vacante',
            name='pregunta',
            field=models.TextField(blank=True),
        ),
    ]
