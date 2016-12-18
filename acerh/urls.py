"""acerh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from users.views import LoginRequest ,LogoutRequest, register
from vacantes.views import vacantelist, aplicado, solicitud, remover, compania, solicitudcompania, userdetail
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/',LoginRequest ),
    url(r'^vacantes/',vacantelist ),
    url(r'^aplicado/',aplicado ),
    url(r'logout/', LogoutRequest, name="logout"),
    url(r'register/$', register),
    url(r'^solicitud/', solicitud, name="solicitud"),
    url(r'^remover/', remover, name="remover"),
    url(r'^compania/',compania ),
    url(r'^solicitudcompania/',solicitudcompania ,name="solicitudcompania" ),
    url(r'^userdetail/',userdetail ,name="userdetail" ),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
