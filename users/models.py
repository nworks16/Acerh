from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db import models

def upload_location(instancia, filename):
	return "CV/%s/%s" %(instancia.id, filename)


# Create your models here.
class UserP(models.Model):
	user = models.OneToOneField(User)
	picture = models.ImageField(upload_to='userpic/', blank=True)
	file = models.FileField(upload_to=upload_location)
	localidad = models.CharField(max_length=100)
	otros = models.CharField(max_length=100)
	mensaje = models.CharField(max_length=100)
	telefono = models.CharField(max_length=15)
	exp = models.CharField(max_length=500)

	def __str__(self):
		return self.user.username

class UserPC(models.Model):
	user = models.OneToOneField(User)
	picture = models.ImageField(upload_to='companypic/', blank=True)
	company = models. BooleanField()
	descripcion = models.TextField()
	
	def __str__(self):
		return self.user.username
