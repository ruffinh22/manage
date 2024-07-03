"""cursusEtu URL Configuration

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
from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from Note import views


urlpatterns = [
    path('importer_csv', views.importer_csv, name='importer_csv'),
    path('suppall', views.suppall, name='suppall'),
    path('', views.listernotes, name='listernotes'),
    path('supprnote/(?P<id>\d+)$', views.supprnote, name='supprnote'),
    path('modifierNote', views.modifierNote, name='modifierNote'),
    path('esultatJury', views.resultatJury, name='resultatJury'),
    path('listerResultat', views.renseignerResultat, name='renseignerResultat'),
    path('completerResultat/(?P<id>\d+)/(?P<Isemestre>\d+)$', views.completerResultat, name='completerResultat'),
    
]
