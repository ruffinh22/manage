#-*- coding: utf-8 -*-
from django.shortcuts import render
from Annee.models import Annee
from Annee.forms import AnneeForm, SelectAnn, RenseignerAnn
from django.shortcuts import render, get_object_or_404
# Create your views here.

"""Cette vue permet d'ajouter une année à la base"""
def ajouterAnnee(request):
	if request.method == 'POST':  
		form = AnneeForm(request.POST)
		if form.is_valid():

			annee = form.cleaned_data['intitule']
			annee_obj = Annee(
					intitule=annee,
	                )
			annee_obj.save()
			res = True
		else :
			print("ERREUR : AJOUTER Annee : VIEW ajouterAnnee : formulaire")
	else :
		form = AnneeForm() 
	return render(request, 'contenu_html/ajouterAnnee.html', locals())

"""Cette vue permet de lister toutes les années présentes dans la base"""
def listerAnnees(request):
	annees = Annee.objects.all()
	return render(request, 'contenu_html/listerAnnees.html', locals())

"""Cette vue permet de supprimer une annee"""
def supprann(request, id):
	annee = Annee.objects.filter(id=id)

	annee.delete()
	return render(request, 'contenu_html/supprann.html', locals())

"""Cette vue permet de modifier une annee"""
def modifierAnnee(request):
	if request.method == 'POST':
		if not request.session['ann']:
			Annees = Annee.objects.all()
			form = SelectAnn(request.POST, annees=Annees)
			if form.is_valid() :
				id_ann = form.cleaned_data['select']
				request.session['id_ann'] = id_ann
				request.session['ann'] = True
			res = True
			a = get_object_or_404(Annee, id=request.session['id_ann'])
			form = RenseignerAnn(annee=a)
		else:
			a = get_object_or_404(Annee, id=request.session['id_ann'])
			form = RenseignerAnn(request.POST, annee=a)
			if form.is_valid() :
				annee = get_object_or_404(Annee, id=request.session['id_ann'])
				if form.cleaned_data['intitule']:
					annee.intitule = form.cleaned_data['intitule']
				annee.save()	
				#request.session['mat'] = False
				res2=True
			else :
				print("ERREUR : MODIFIER Annee : VIEW modifierAnnee : formulaire")	
	else :
		Annees = Annee.objects.all()
		request.session['ann'] = False
		form = SelectAnn(annees=Annees)
	return render(request, 'contenu_html/modifierAnnee.html', locals())