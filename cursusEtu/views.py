#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

"""Cette vue permet de faire afficher l'accueil"""
def accueil(request):
	return render(request, 'templates/contenu_html/accueil.html')

"""Cette vue permet de faire afficher la page d'aides"""
def aides(request):
	return render(request, 'templates/contenu_html/aides.html')

"""Cette vue permet de faire passer la variable de session de modeAdmin a True"""
def onAdmin(request):
	try:
		if request.session['admin']:
			request.session['admin'] = False
		else:
			request.session['admin'] = True
	except:
		request.session['admin'] = True
	finally:
		return HttpResponse("<p>Ok</p>")
