#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from UE.models import UE
from Semestre.models import Semestre
from Matiere.models import Matiere
from UE.forms import UEForm, SelectSemestre,SelectUE,RenseignerUe


# Create your views here.

"""Cette fonction permet de faire afficher toutes les UE"""
def listerUE(request):
	ues = UE.objects.all()
	return render(request, 'contenu_html/listerUE.html',{'ues': ues})

"""Cette fonction permet de supprimer une ue"""
def supprue(request, id):
	ue = UE.objects.filter(id=id)

	matiere = Matiere.objects.filter(ue_id=id)

	if matiere :
		matiere.delete()

	ue.delete()
	return render(request, 'contenu_html/supprue.html', locals())


"""Cette fonction permet de faire afficher les matieres et les details d'une ue"""
def detailUE(request, id):
	ue = get_object_or_404(UE, id=id)
	matieres = Matiere.objects.filter(ue__id=id)
	return render(request, 'contenu_html/detailUE.html', locals())

"""Cette vue permet d ajouter une UE a la base"""
def ajouterUE(request):

	if request.method == 'POST':

		if not request.session['sem']:
			sem = Semestre.objects.all()
			form = SelectSemestre(request.POST, semestres = sem)
			if form.is_valid() :
				id_sem = form.cleaned_data['select']
				request.session['id_sem'] = id_sem
				request.session['sem'] = True
				res = True
			e = get_object_or_404(Semestre, id=request.session['id_sem'])
			form=UEForm()
		else:
			form = UEForm(request.POST)
			if form.is_valid() :
				intitule = form.cleaned_data['intitule']
				code_ppn = form.cleaned_data['code_ppn']
				code_apogee = form.cleaned_data['code_apogee']
				s = get_object_or_404(Semestre, id=request.session['id_sem'])
				coef = form.cleaned_data['coefficient']
				ue = UE(
						intitule=intitule,
						code_ppn=code_ppn,
						code_apogee=code_apogee,
						semestre=s,
						coefficient=coef,
		                )
				ue.save()
				request.session['sem'] = False
				res2=True
			else :
				print("ERREUR")	
	else :
		sem = Semestre.objects.all()
		request.session['sem'] = False
		form = SelectSemestre(semestres = sem)
	return render(request, 'contenu_html/ajouterUE.html', locals())

"""Cette vue permet de modifier une ue"""
def modifierUe(request):
	if request.method == 'POST':
		if not request.session['ue']:
			Unites = UE.objects.all()
			form = SelectUE(request.POST, ues=Unites)
			if form.is_valid() :
				id_ue = form.cleaned_data['select']
				request.session['id_ue'] = id_ue
				request.session['ue'] = True
			res = True
			u = get_object_or_404(UE, id=request.session['id_ue'])
			form = RenseignerUe(ue=u)
		else:
			u = get_object_or_404(UE, id=request.session['id_ue'])
			form = RenseignerUe(request.POST, ue=u)
			if form.is_valid() :
				unite = get_object_or_404(UE, id=request.session['id_ue'])
				if form.cleaned_data['intitule']:
					unite.intitule = form.cleaned_data['intitule']
				if form.cleaned_data['coefficient']:
					unite.coefficient = form.cleaned_data['coefficient']
				if form.cleaned_data['code_ppn']:
					unite.code_ppn = form.cleaned_data['code_ppn']
				if form.cleaned_data['code_apogee']:
					unite.code_apogee = form.cleaned_data['code_apogee']
				if form.cleaned_data['semestre']:
					unite.semestre = form.cleaned_data['semestre']
				unite.save()	
				#request.session['mat'] = False
				res2=True
			else :
				print("ERREUR : MODIFIER Ue : VIEW modifierUe : formulaire ")	
	else :
		Unites = UE.objects.all()
		request.session['ue'] = False
		form = SelectUE(ues=Unites)
	return render(request, 'contenu_html/modifierUe.html', locals())
