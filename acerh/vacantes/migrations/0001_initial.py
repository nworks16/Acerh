# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 02:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aplicado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Estatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=20)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Vacante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('picturep', models.ImageField(blank=True, upload_to='vacantes/')),
                ('creatd_date', models.DateTimeField(auto_now_add=True)),
                ('vigencia', models.CharField(max_length=100)),
                ('requisitos', models.TextField()),
                ('pregunta', models.CharField(max_length=100)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacantes.Area')),
                ('compania', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vacantes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('picturep', models.ImageField(blank=True, upload_to='vacantes/')),
                ('creatd_date', models.DateTimeField(auto_now_add=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacantes.Area')),
                ('compania', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='aplicado',
            name='aplico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacantes.Vacantes'),
        ),
        migrations.AddField(
            model_name='aplicado',
            name='estatus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacantes.Estatus'),
        ),
        migrations.AddField(
            model_name='aplicado',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]