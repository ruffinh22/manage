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
from UE import views


urlpatterns = [

    path('isterUE$', views.listerUE, name='listerUE'),
    path('detailUE/(?P<id>\d+)$', views.detailUE, name='detailUE'),
    path('ajouterUE', views.ajouterUE, name='ajouterUE'),
    path('supprue/(?P<id>\d+)$', views.supprue, name='supprue'),
    path('modifierUe', views.modifierUe, name='modifierUe'),
]
