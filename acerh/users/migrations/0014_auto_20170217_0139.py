# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-17 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_userp_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='userp',
            name='edad',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userp',
            name='estudio',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userp',
            name='experiencia',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='userp',
            name='localidad',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
