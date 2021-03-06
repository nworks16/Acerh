# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect ,HttpResponse
from users.forms import LoginForm ,UserP, UsuarioForm2, UserPr,PasswordResetRequestForm,SetPasswordForm, UsuarioForm, UserPr2,UserPr3
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login,logout
from vacantes.models import Vacante, Aplicado, Provincia, Area
from django.db import models
from users.models import UserPC, UserP
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from smtplib import SMTPRecipientsRefused
from django.core.mail import EmailMultiAlternatives
from django.core.mail.message import EmailMessage
from django.template import Library
from django.template.defaulttags import cycle as cycle_original
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static
from xlsxwriter.workbook import Workbook
import sys
import StringIO
import io
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sys
import unicodedata
from django.utils.dateparse import parse_date
import datetime
from django.utils.timezone import now
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from django import template
# Create your views here.





def idioma(request):
	context = {

	}

	return render(request, 'idioma.html', context)


def user_detail(request, id=None):
	cliente = get_object_or_404(User, id=id)
	profile = get_object_or_404(User, id=id)
	aplicado = Aplicado.objects.filter(usuario=id)
	context = {
		"cliente":cliente,
		"profile":profile,
		"aplicado":aplicado, "aplicados":aplicado.all()
	}

	return render(request, 'profile2.html', context)



@csrf_protect
def LoginRequest(request):
	message = "Credenciales invalidas o No registradas"
	# Si el usuario ya ha iniciado sesion anteriormente.
	if request.user.is_authenticated():
		return HttpResponseRedirect('/vacantes')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		# Si el formulario es valido, iniciar la sesion y redireccionar
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			usuario = authenticate(username=username,password=password)
			if usuario is not None:
				login(request,usuario)
				if request.user.is_staff:

					return HttpResponseRedirect('/compania')
				else:
					if request.user.userp.pais_apli == 'Jamaica' or request.user.userp.pais_apli == 'Trinidad y Tobago':
						return HttpResponseRedirect('/vacantes2')
					else:
						return HttpResponseRedirect('/vacantes')
			# De lo contrario devolver al Login
			else:
				render(request, "loginmaterial.html", {'form':form})
				return render(request, "loginmaterial.html", {'form':form, 'message':message})
		# Si el formulario es invalido devolver al login
		else:

			return render(request, "loginmaterial", {'form':form } )
	else:
		form = LoginForm()
		context = {'form':form}
		return render(request, "loginmaterial.html", {'form':form})


def LogoutRequest(request):
	logout(request)
	return HttpResponseRedirect('/login')




def register(request):
	context = RequestContext(request)
	registered = False
	area = Area.objects.all()
	provincia = Provincia.objects.all()
	message = ""
	if request.method == 'POST':
		user_form = UsuarioForm2(data=request.POST)
		profile_form = UserPr(data=request.FILES)
		data2 = request.POST.get('username')
		if User.objects.filter(username=data2).exists():
			message = "Este Username ya se encuentra en uso, intente otro"
			return render (request,'registromaterial.html',{'user_form':user_form, 'profile_form': profile_form, 'message':message})


		data = request.POST['email']
		if User.objects.filter(email=data).exists():
			message = "Este correo electronico fue regustrado"
			return render (request,'registromaterial.html',{'user_form':user_form, 'profile_form': profile_form, 'message':message})



		else:
			if user_form.is_valid() and profile_form.is_valid():
				user = user_form.save()
				user.set_password(user.password)
				user.save()
				profile = profile_form.save(commit=False)
				profile.user = user
				profile.save()
				registered = True
				username = user_form.cleaned_data['username'].encode('utf8')
				password = user_form.cleaned_data['password'].encode('utf8')
				if 'file' in request.FILES:
					profile.file = request.FILES['file']
				else:
					profile.file = static('/nocv.txt')

				if 'picture' not in request.FILES:
					profile.picture =  static('/user.png')
				else:
					profile.picture = request.FILES['picture']

				profile.cedula = unicodedata.normalize('NFKD', request.POST.get('cedula')).encode('ascii', 'ignore')
				profile.sexo = unicodedata.normalize('NFKD', request.POST.get('sexo')).encode('ascii', 'ignore')
				profile.idioma = request.GET.getlist('idioma')

				print dict(request.POST)["idioma"]	
				profile.idioma = dict(request.POST)["idioma"]				
				profile.carrera = unicodedata.normalize('NFKD', request.POST.get('carrera')).encode('ascii', 'ignore')
				print dict(request.POST)["carrera"]	
				profile.ar_int = dict(request.POST)["ar_int"]	
				profile.salario = unicodedata.normalize('NFKD', request.POST.get('salario')).encode('ascii', 'ignore')
				profile.telefono = request.POST.get('telefono').encode('utf8')
				profile.localidad = unicodedata.normalize('NFKD', request.POST.get('localidad')).encode('ascii', 'ignore')
				profile.estudio = unicodedata.normalize('NFKD', request.POST.get('estudio')).encode('ascii', 'ignore')
				profile.edad = unicodedata.normalize('NFKD', request.POST.get('edad')).encode('ascii', 'ignore')

				#profile.edad = calculate_age(datetime.datetime.strptime(request.POST.get('edad'), "%d-%m-%Y").date())
				profile.edad = unicodedata.normalize('NFKD', request.POST['edad']).encode('ascii', 'ignore')
				
				profile.experiencia = unicodedata.normalize('NFKD', request.POST.get('experiencia')).encode('ascii', 'ignore')
				profile.nacionalidad = unicodedata.normalize('NFKD', request.POST.get('nacionalidad')).encode('ascii', 'ignore')
				profile.universidad = unicodedata.normalize('NFKD', request.POST.get('universidad')).encode('ascii', 'ignore')
				profile.licencia = unicodedata.normalize('NFKD', request.POST.get('licencia')).encode('ascii', 'ignore')
				profile.cat_licen = unicodedata.normalize('NFKD', request.POST.get('cat_licen')).encode('ascii', 'ignore')
				profile.pais_apli = unicodedata.normalize('NFKD', request.POST.get('pais_apli')).encode('ascii', 'ignore')

				profile.save()
				usuario = authenticate(username=username,password=password)
				login(request,usuario)
				return HttpResponseRedirect('/vacantes')

	else:
		user_form = UsuarioForm2()
		profile_form = UserPr()
		area = Area.objects.all()
		provincia = Provincia.objects.all()
		return render (request,'registromaterial.html',{'user_form':user_form, 'profile_form': profile_form,'area':area,'areas':area.all(),'provincia':provincia,'provincias':provincia.all()})


def register2(request):
	context = RequestContext(request)
	registered = False
	area = Area.objects.all()
	provincia = Provincia.objects.all()
	message = ""
	if request.method == 'POST':
		user_form = UsuarioForm2(data=request.POST)
		profile_form = UserPr(data=request.FILES)
		data2 = request.POST['username']
		if User.objects.filter(username=data2).exists():
			message = "This Username is already in use, try another"
			return render (request,'registerbeta2.html',{'user_form':user_form, 'profile_form': profile_form, 'message':message})


		data = request.POST['email']
		if User.objects.filter(email=data).exists():
			message = "This email was registered"
			return render (request,'registerbeta2.html',{'user_form':user_form, 'profile_form': profile_form, 'message':message})



		else:
			if user_form.is_valid() and profile_form.is_valid():
				user = user_form.save()
				user.set_password(user.password)
				user.save()
				profile = profile_form.save(commit=False)
				profile.user = user
				profile.save()
				registered = True
				username = user_form.cleaned_data['username'].encode('utf8')
				username = username.decode('unicode_escape').encode('ascii','ignore')
				password = user_form.cleaned_data['password'].encode('utf8')
				if 'file' in request.FILES:
					profile.file = request.FILES['file']
				else:
					profile.file = static('/nocv.txt')

				if 'picture' not in request.FILES:
					profile.picture =  static('/user.png')
				else:
					profile.picture = request.FILES['picture']

				profile.cedula = unicodedata.normalize('NFKD', request.POST['cedula']).encode('ascii', 'ignore')
				profile.sexo = unicodedata.normalize('NFKD', request.POST['sexo']).encode('ascii', 'ignore')
				profile.idioma = unicodedata.normalize('NFKD', request.POST['idioma']).encode('ascii', 'ignore')
				profile.carrera = unicodedata.normalize('NFKD', request.POST['carrera']).encode('ascii', 'ignore')
				profile.ar_int = unicodedata.normalize('NFKD', request.POST['ar_int']).encode('ascii', 'ignore')
				profile.salario = unicodedata.normalize('NFKD', request.POST['salario']).encode('ascii', 'ignore')
				profile.telefono = request.POST['telefono'].encode('utf8')
				profile.localidad = unicodedata.normalize('NFKD', request.POST['localidad']).encode('ascii', 'ignore')
				profile.estudio = unicodedata.normalize('NFKD', request.POST['estudio']).encode('ascii', 'ignore')
				profile.edad = unicodedata.normalize('NFKD', request.POST['edad']).encode('ascii', 'ignore')
				profile.experiencia = unicodedata.normalize('NFKD', request.POST['experiencia']).encode('ascii', 'ignore')
				profile.nacionalidad = unicodedata.normalize('NFKD', request.POST['nacionalidad']).encode('ascii', 'ignore')
				profile.universidad = unicodedata.normalize('NFKD', request.POST['universidad']).encode('ascii', 'ignore')
				profile.licencia = unicodedata.normalize('NFKD', request.POST['licencia']).encode('ascii', 'ignore')
				profile.cat_licen = unicodedata.normalize('NFKD', request.POST['cat_licen']).encode('ascii', 'ignore')
				profile.pais_apli = unicodedata.normalize('NFKD', request.POST['pais_apli']).encode('ascii', 'ignore')

				profile.save()
				usuario = authenticate(username=username,password=password)
				login(request,usuario)
				return HttpResponseRedirect('/vacantes2')

	else:
		user_form = UsuarioForm2()
		profile_form = UserPr()
		area = Area.objects.all()
		provincia = Provincia.objects.all()
		return render (request,'registerbeta2.html',{'user_form':user_form, 'profile_form': profile_form,'area':area,'areas':area.all(),'provincia':provincia,'provincias':provincia.all()})




def userdetail2(request):
	userinfo = User.objects.get(id=request.user.id)
	aplicado = Aplicado.objects.filter(usuario=request.user)
	cantidad = aplicado.count()
	userdetalle = UserP.objects.filter(user=request.user)
	context = { "aplicado":aplicado, "aplicados":aplicado.all() ,"cantidad":cantidad,"userdetalle":userdetalle,"userdetalles":userdetalle.all()}
	context2 = RequestContext(request)
	registered = False
	if request.method == 'POST':
		user_form = UsuarioForm(data=request.POST)
		profile_form = UserPr(data=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():

			user = user_form.save()
			user.username = request.user.username
			user.save()
			profile = profile_form.save(commit=False)
			profile.file = request.FILES['file']
			profile.localidad = request.POST['localidad']
			profile.estudio = request.POST['estudio']
			profile.edad = request.POST['edad']
			profile.experiencia = request.POST['experiencia']

			profile.user = user
			profile.save()
			registered = True
	return render(request, 'profile.html', context, {'user_form':user_form,'profile_form':profile_form})


def userdetail(request):
	area = Area.objects.all()
	provincia = Provincia.objects.all()
	userinfo = User.objects.get(id=request.user.id)
	aplicado = Aplicado.objects.filter(usuario=request.user)
	cantidad = aplicado.count()
	userdetalle = UserP.objects.get(user=request.user)
	user_form = UsuarioForm(data=request.POST, instance=userinfo)
	profile_form = UserPr3(data=request.POST,files=request.FILES, instance=userdetalle)
	if request.method == 'POST':

		if user_form.is_valid() and profile_form.is_valid():
			profile = profile_form.save(commit=False)
			if 'file' in request.FILES:
				profile.file = request.FILES['file']
			else:
				if request.user.userp.file:
					profile.file = request.user.userp.file
				else:
					profile.file = static('/nocv.txt')

			if 'picture' not in request.FILES:
				if request.user.userp.file:
					profile.picture = request.user.userp.picture
				else:
					profile.picture =  static('/user.png')
			else:
				profile.picture = request.FILES['picture']

			user = user_form.save()
			if 'first_name' in request.POST:
				user.first_name = request.POST['first_name']
			else:
				user.first_name = request.user.first_name

			if 'last_name' in request.POST:
				user.last_name = request.POST['last_name']
			else:
				user.last_name = request.user.last_name

			if 'email' in request.POST:
				user.email = request.POST['email']
			else:
				user.email = request.user.email

			user.username = request.user.username
			user.save()


			profile.cedula = request.POST['cedula']
			profile.sexo = request.POST['sexo']
			profile.idioma = request.POST['idioma']
			profile.carrera = request.POST['carrera']
			profile.ar_int = request.POST['ar_int']
			profile.salario = request.POST['salario']
			profile.telefono = request.POST['telefono']
			profile.localidad = request.POST['localidad']
			profile.estudio = request.POST['estudio']
			profile.edad = request.POST['edad']
			profile.experiencia = request.POST['experiencia']
			profile.nacionalidad = request.POST['nacionalidad']
			profile.universidad = request.POST['universidad']
			profile.licencia = request.POST['licencia']
			profile.cat_licen = request.POST['cat_licen']
			profile.pais_apli = request.POST['pais_apli']

			profile.user = user
			profile.save()
			registered = True
			return HttpResponseRedirect('/userdetail')
		else:
			user_form = UsuarioForm(data=request.POST, instance=userinfo)
			profile_form = UserPr3(data=request.POST,files=request.FILES, instance=userinfo)
	return render(request, 'profile.html', {'user_form':user_form,'profile_form':profile_form, 'aplicado':aplicado, 'aplicados':aplicado.all(),'area':area, 'areas':area.all(), 'provincia':provincia,'provincias':provincia.all()})


def email(request):
	email = EmailMessage()
	email.subject = "Hola mensaje de prueba desde el servidor de acerh"
	email.body = "Coneccion totalmente lograda, prueba test #2"
	email.to = [ "nworks16@gmail.com"]
	email.send()

import json
def consulta(request):
	search_text = request.GET.get('ajax')
	array = []
	print search_text
	if search_text is not None:
		if request.is_ajax():
			clientes = User.objects.filter(email=search_text)
			if clientes.exists():
				print "Existe"
				array = []
				array.insert(0,"This Email Exists, Use Other")
				return HttpResponse(json.dumps( list(array)), content_type='application/json' )
			else:
				print "No Existe"
				try:
					email = EmailMessage()
					email.subject = "METODO VERIFICACION ACERH"
					email.body = "This is an automatic email generated by the application of ACERHGROUP to verify emails, please ignore this email"
					email.to = [ search_text ]
					email.send()
					array.insert(0,"This Email is Available")
				except:

					array.insert(0,"This email is not real or does not exist")
				return HttpResponse( json.dumps( list(array)), content_type='application/json' )
	else:
		return HttpResponse("")

def consultaur(request):
	search_text = request.GET.get('ajax')
	print search_text
	if search_text is not None:
		if request.is_ajax():
			clientes = User.objects.filter(username=search_text)
			if clientes.exists():
				print "Existe"
				array = []
				array.insert(0,"Este Username Existe, Use Otro")
				return HttpResponse(json.dumps( list(array)), content_type='application/json' )
			else:
				print "No Existe"
				array = []
				array.insert(0,"Este Username Esta Disponible")
				return HttpResponse( json.dumps( list(array)), content_type='application/json' )
	else:
		return HttpResponse("")


def consultan(request):
	search_text = request.GET.get('ajax')
	print search_text
	if search_text is not None:
		if request.is_ajax():
			clientes = User.objects.filter(username=search_text)
			if clientes.exists():
				print "Existe"
				array = []
				array.insert(0,"Este Username Esta en Uso,Ingrese Otro")
				return HttpResponse(json.dumps( list(array)), content_type='application/json' )
			else:
				print "No Existe"
				array = []
				array.insert(0,"Este Username Esta Disponible")
				return HttpResponse( json.dumps( list(array)), content_type='application/json' )
	else:
		return HttpResponse("")

from django.core import serializers
def consultauser(request):
	search_text = request.GET.get('ajax')
	print search_text
	if search_text is not None:
		if request.is_ajax():
			clientes = User.objects.filter(first_name__icontains=search_text)
			if clientes.exists():
				data = serializers.serialize("json", clientes)
				for cliente in clientes:
					print cliente.username
					array = []
					array.insert(0,cliente.id)
				return HttpResponse(json.dumps(list(clientes.values('pk','first_name', 'last_name','email'))), content_type='application/json' )
			else:
				print "No Existe"
				array = []
				array.insert(0,"Este Username Esta Disponible")
				return HttpResponse( json.dumps( list(array)), content_type='application/json' )
	else:
		return HttpResponse("")


from collections import OrderedDict

from django import forms
from django.core.mail import EmailMultiAlternatives
from django.forms.utils import flatatt
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from django.views.generic import *

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

class ResetPasswordRequestView(FormView):
	template_name = "test_template.html"    #code for template is given below the view's code
	success_url = '/vacantes'
	form_class = PasswordResetRequestForm
	@staticmethod
	def validate_email_address(email):
		try:
			validate_email(email)
			return True
		except ValidationError:
			return False
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			data= form.cleaned_data["email_or_username"]
		if self.validate_email_address(data) is True:                 #uses the method written above
			'''
			If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
			'''
			associated_users= User.objects.filter(Q(email=data)|Q(username=data))
			if associated_users.exists():
				for user in associated_users:
						c = {
							'email': user.email,
							'domain': request.META['HTTP_HOST'],
							'site_name': 'your site',
							'uid': urlsafe_base64_encode(force_bytes(user.pk)),
							'user': user,
							'token': default_token_generator.make_token(user),
							'protocol': 'http',
							}
						subject_template_name='registration/password_reset_subject.txt'
						# copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
						email_template_name='registration/password_reset_email.html'
						# copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
						subject = loader.render_to_string(subject_template_name, c)
						# Email subject *must not* contain newlines
						subject = ''.join(subject.splitlines())
						email = loader.render_to_string(email_template_name, c)
						send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
				result = self.form_valid(form)
				messages.success(request, 'Email a sido enviado a ' + data +". direccion de correo. por favor revise su imbox para continuar con el registro.")
				return result
			result = self.form_invalid(form)
			messages.error(request, 'Este Username no existe en el sistema')
			return result
		else:
			'''
			If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
			'''
			associated_users= User.objects.filter(username=data)
			if associated_users.exists():
				for user in associated_users:
					c = {
						'email': user.email,
						'domain': 'example.com', #or your domain
						'site_name': 'example',
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'user': user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
						}
					subject_template_name='registration/password_reset_subject.txt'
					email_template_name='registration/password_reset_email.html'
					subject = loader.render_to_string(subject_template_name, c)
					# Email subject *must not* contain newlines
					subject = ''.join(subject.splitlines())
					email = loader.render_to_string(email_template_name, c)
					send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
				result = self.form_valid(form)
				messages.success(request, 'Email a sido enviado a' + data +"'s direccion de correo. por favor revise su imbox para continuar con el registro.")
				return result
			result = self.form_invalid(form)
			messages.error(request, 'Este Username no existe en el sistema.')
			return result
		messages.error(request, 'Invalid Input')
		return self.form_invalid(form)

class PasswordResetConfirmView(FormView):
	template_name = "test_template.html"
	success_url = '/login'
	form_class = SetPasswordForm

	def post(self, request, uidb64=None, token=None, *arg, **kwargs):
		"""
		View that checks the hash in a password reset link and presents a
		form for entering a new password.
		"""
		UserModel = get_user_model()
		form = self.form_class(request.POST)
		assert uidb64 is not None and token is not None  # checked by URLconf
		try:
			uid = urlsafe_base64_decode(uidb64)
			user = UserModel._default_manager.get(pk=uid)
		except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
			user = None

		if user is not None and default_token_generator.check_token(user, token):
			if form.is_valid():
				new_password= form.cleaned_data['new_password2']
				user.set_password(new_password)
				user.save()
				messages.success(request, 'Password fue reiniciado.')
				return self.form_valid(form)
			else:
				messages.error(request, 'Password no pudo cambiarse.')
				return self.form_invalid(form)
		else:
			messages.error(request,'El enlace de reinicio ya no es valido.')
			return self.form_invalid(form)

#FUNCION ENCARGADA DE LA CREACION DEL REPORTE EN EXCEL
def export_excel(request):
	#Llamada a la libreria para escribir en bits
	output = io.BytesIO()

	#Se inicializa el workbook de excel en cache
	workbook = Workbook(output, {'in_memory': True})
	worksheet = workbook.add_worksheet()

	#se setea la variable cell con 8 para que empieze a escribir desde la celda 8
	cell = 8
	#ciclo que busca todos los objetos con estatus 195(por enviar) para ser escritos en el excel
	for obj in User.objects.all():
		#indica desde que celda se escribe el titulo de los id de los objetos
		worksheet.write_string(cell,0, str(obj.id))
		#indica desde que celda se escribiran los emails
		worksheet.write_string(cell,1, obj.email)
		#indica desde que celda se escribiran los codigos de pss
		worksheet.write_string(cell,2, str(obj.first_name).encode('ascii','ignore'))
		#indica desde que celda se escribiran la ruta de los archivos
		worksheet.write_string(cell,3, (obj.last_name).encode('ascii','ignore'))
		#escribre el username
		worksheet.write_string(cell,4, (obj.username).encode('ascii','ignore'))

		#Se realiza el aumento de la celda para seguir escribiendo hacia abajo
		cell = cell + 1




	#Variable que define el estilo de negrita
	bold = workbook.add_format({'bold': 1}) #letra negrita
	#Variable que define el tamanio de las letras
	size = workbook.add_format({'font_size': 20})
	#Define el color rojo de las celdas
	green = workbook.add_format({'bg_color': 'red', 'bold': 1})
	#Escriben los enunciados del reporte de excel y ejecuta el logo
	worksheet.write('C5', 'Reporte en excel de Acerh, Todos los usuarios',size)
	worksheet.insert_image('B4', 'static/plugins/logo2.png', {'x_scale': 0.3, 'y_scale': 0.3})
	worksheet.set_column('A:A', 5)
	worksheet.write('A8', 'ID',green)
	worksheet.set_column('B:B', 50)
	worksheet.write('B8', 'Correo',green)
	worksheet.set_column('C:C', 40)
	worksheet.write('C8', 'Primer Nombre',green)
	worksheet.set_column('D:D', 100)
	worksheet.write('D8', 'Apellidos',green)
	worksheet.set_column('E:E', 100)
	worksheet.write('E8', 'Username',green)



	#worksheet.add_table('B3:F7') #TABLA
	#Cierra el workbook del excel para ser guardado
	workbook.close()

	output.seek(0)
	#response que contiene el archivo xlsx que sera devuelto a la ventana del navegador
	response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment; filename=UserReport.xlsx"

	#funcion de retorno
	return response


def export_excel2(request):
	#Llamada a la libreria para escribir en bits
	output = io.BytesIO()

	#Se inicializa el workbook de excel en cache
	workbook = Workbook(output, {'in_memory': True})
	worksheet = workbook.add_worksheet()

	#se setea la variable cell con 8 para que empieze a escribir desde la celda 8
	cell = 8
	#ciclo que busca todos los objetos con estatus 195(por enviar) para ser escritos en el excel
	for obj in UserP.objects.filter(localidad=""):
		userm = User.objects.get(username=obj.user).encode('utf-8')
		#indica desde que celda se escribe el titulo de los id de los objetos
		worksheet.write_string(cell,0, str(obj.id)).encode('utf-8')
		#indica desde que celda se escribiran los emails
		worksheet.write_string(cell,1, str(obj.user)).encode('utf-8')
		#indica desde que celda se escribiran los codigos de pss
		worksheet.write_string(cell,2, str(userm.email)).encode('utf-8')
		#indica desde que celda se escribiran la ruta de los archivos
		worksheet.write_string(cell,3, str(userm.first_name)).encode('utf-8')
		#escribre el username
		worksheet.write_string(cell,4, str(userm.last_name)).encode('utf-8')

		#Se realiza el aumento de la celda para seguir escribiendo hacia abajo
		cell = cell + 1




	#Variable que define el estilo de negrita
	bold = workbook.add_format({'bold': 1}) #letra negrita
	#Variable que define el tamanio de las letras
	size = workbook.add_format({'font_size': 20})
	#Define el color rojo de las celdas
	green = workbook.add_format({'bg_color': 'red', 'bold': 1})
	#Escriben los enunciados del reporte de excel y ejecuta el logo
	worksheet.write('C5', 'Reporte en excel de Acerh, Usuarios Perfiles en blanco',size)
	worksheet.insert_image('B4', 'static/plugins/logo2.png', {'x_scale': 0.3, 'y_scale': 0.3})
	worksheet.set_column('A:A', 5)
	worksheet.write('A8', 'ID',green)
	worksheet.set_column('B:B', 50)
	worksheet.write('B8', 'UserName',green)
	worksheet.set_column('C:C', 40)
	worksheet.write('C8', 'Correo',green)
	worksheet.set_column('D:D', 40)
	worksheet.write('D8', 'Nombres',green)
	worksheet.set_column('E:E', 100)
	worksheet.write('E8', 'Apellidos',green)



	#worksheet.add_table('B3:F7') #TABLA
	#Cierra el workbook del excel para ser guardado
	workbook.close()

	output.seek(0)
	#response que contiene el archivo xlsx que sera devuelto a la ventana del navegador
	response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment; filename=UserReport.xlsx"

	#funcion de retorno
	return response


from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class logouttk(APIView):
	queryset = User.objects.all()

	def get(self, request, format=None):
		# simply delete the token to force a login
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import JsonResponse

@csrf_exempt
def usermov(request):
	#Obtener el usuario del json movil
	print "PRINT JSON"
	print request.body
	data3 = json.loads(request.body)
	print json.loads(request.body)
	mouser = Token.objects.get(key=data3["token"])
	print "mouser" , mouser.user.id
	userbasic = User.objects.get(id=mouser.user.id)
	print userbasic
	userpro = UserP.objects.get(user=userbasic)
	vacante_dict = {}
	Registros=[]
	domain = request.get_host()
	record = { "id":userbasic.id, "user":userbasic.username, "first_name":userbasic.first_name, "last_name":userbasic.last_name, "email":userbasic.email, "picture":"http://"+domain+userpro.picture.url,"localidad":userpro.localidad, "estudio":userpro.estudio,"edad":userpro.edad,"experiencia":userpro.experiencia,"idioma":userpro.idioma,"ar_int":userpro.ar_int,"carrera":userpro.carrera,"sexo":userpro.sexo,"cedula":userpro.cedula, "nacionalidad":userpro.nacionalidad,"universidad":userpro.universidad,"pais_apli":userpro.pais_apli,"telefono":userpro.telefono}
	Registros.append(record)
	pickup_records = json.dumps(Registros)
	pickup_response={"registros":Registros}


	return JsonResponse(pickup_response, safe=False)


@csrf_exempt
def loginmov(request):
	#Obtener el usuario del json movil
	print "PRINT JSON"
	print request.body
	data3 = json.loads(request.body)
	print json.loads(request.body)
	usuario = authenticate(username=data3["username"],password=data3["password"])
	if usuario is not None:
		print usuario
		print usuario.username
		user = Token.objects.get(user=usuario)
		print user
		print user.key
		return HttpResponse(json.dumps({"Token":user.key}), content_type='application/json')
	else:
		return HttpResponse(json.dumps("Rejected"), content_type='application/json')




from django.contrib.auth.hashers import make_password

@csrf_exempt
def registermov(request):
	data3 = json.loads(request.body)
	print json.loads(request.body)
	print data3["username"]
	print data3["first_name"]
	print data3["last_name"]
	print data3["password"]
	print data3["email"]
	print data3["cedula"]
	print data3["sexo"]
	print data3["idioma"]
	print data3["carrera"]
	print data3["ar_int"]
	print data3["salario"]
	print data3["telefono"]
	print data3["localidad"]
	print data3["estudio"]
	print data3["edad"]
	print data3["experiencia"]
	print data3["nacionalidad"]
	print data3["universidad"]
	print data3["licencia"]
	print data3["cat_licen"]
	print data3["pais_apli"]

	if User.objects.filter(username=data3["username"]).exists():
		message = "Este Username:" + " " + data3["username"] + " " + " ya se encuentra en uso, intente otro"  
		return HttpResponse(json.dumps(message), content_type='application/json')


	if User.objects.filter(email=data3["email"]).exists():
		message = "Este correo electronico fue registrado"
		return HttpResponse(json.dumps(message), content_type='application/json')
	
	user = User.objects.create_user(username=data3["username"],first_name=data3["first_name"],last_name=data3["last_name"],email=data3["email"],password=data3["password"],is_active=True).save()
	
	user2 = User.objects.get(username=data3["username"])
	
	print user2

	user3 = Token.objects.create(user=user2)
	
	print user3
	print user3.key


	userp = UserP.objects.create(user=user2,cedula=data3["cedula"],sexo=data3["sexo"],idioma=data3["idioma"],carrera=data3["carrera"],ar_int=data3["ar_int"],salario=data3["salario"],telefono=data3["telefono"],localidad=data3["localidad"],estudio=data3["estudio"],edad=data3["edad"],experiencia=data3["experiencia"],nacionalidad=data3["nacionalidad"],universidad=data3["universidad"],licencia=data3["licencia"],cat_licen=data3["cat_licen"],pais_apli=data3["pais_apli"])

	return HttpResponse(json.dumps("Registered"), content_type='application/json')


@csrf_exempt
def registerconmov(request):
	#Obtener el usuario del json movil
	area_dict = {}
	Areas=[]
	vjs = Area.objects.all()
	print vjs
	for tmpPickUp in vjs:
		record = {"titulo":tmpPickUp.titulo, "id":tmpPickUp.id}
		Areas.append(record)
		pickup_records = json.dumps(Areas)
		pickup_response={"areas":Areas}
	return JsonResponse(pickup_response, safe=False)



from django.http.multipartparser import MultiPartParser
import base64,uuid
from django.core.files.base import ContentFile


@csrf_exempt
def avatarmov(request):
	print 'request cvmov'
	img64 = request.POST['file']
	cv64 = request.POST['cv']
	typefile = request.POST['type']
	token = request.POST['token']
	print request.POST.keys()
	print typefile
	print token

	try:
		#Conversion de Base64 a la imagen
		format, imgstr = img64.split(';base64,') 
		ext = format.split('/')[-1] 
		id = uuid.uuid4()

		data = ContentFile(base64.b64decode(imgstr), name=id.urn[9:] + '.' + ext)

		usuario = Token.objects.get(key=token)

		print usuario

		userpro = UserP.objects.get(user=usuario.user)
		userpro.picture = data


		#Conversion de Bas64 a el archivo
		format, cvstr = cv64.split(';base64,') 
		id2 = uuid.uuid4()

		data2 = ContentFile(base64.b64decode(cvstr), name=id2.urn[9:] + '.' + typefile)

		userpro.file = data2
		userpro.save()

		return HttpResponse(json.dumps({"msg":'done'}), content_type='application/json')
	except:
		return HttpResponse(json.dumps({"msg":'error'}), content_type='application/json')
