#-*- coding: utf-8 -*-
from django.shortcuts import render
from Semestre.models import Semestre, InstanceSemestre
from Semestre.forms import SemestreForm, SelectSem, RenseignerSem,InstanceSemestreForm,SelectInstanceSemestre,EvolutionSemestreForm
from UE.models import UE
from Matiere.models import Matiere
from django.shortcuts import render, get_object_or_404
from Etudiant.models import Appartient, Etu
from Note.models import Resultat_Semestre
from Diplome.models import Diplome
# Create your views here.

"""Cette vue permet d'ajouter un semestre"""
def ajouterSemestre(request):
	if request.method == 'POST':
		form = SemestreForm(request.POST)
		if form.is_valid():

			code_ppn = form.cleaned_data['code_ppn']
			code_apogee = form.cleaned_data['code_apogee']
			dip = form.cleaned_data['diplome']
			intitule = form.cleaned_data['intitule']
			sem = Semestre(
					code_ppn=code_ppn,
					code_apogee=code_apogee,
					intitule=intitule,
					diplome = dip,
	                )
			sem.save()
			res = True
		else :
			print("ERREUR : AJOUTER Semestre : VIEW ajouterUE : formulaire")
	else :
		diplomes = Diplome.objects.all()
		form = SemestreForm(diplomes=diplomes)
	return render(request, 'contenu_html/ajouterSemestre.html', locals())

"""Cette vue permet de lister les semestres"""
def listerSemestre(request):
	semestre = Semestre.objects.all()
	return render(request, 'contenu_html/listerSemestre.html',{'semestre': semestre})

"""Cette vue permet de supprimer un semestre"""
def supprsem(request, id):
	semestre = Semestre.objects.filter(id=id)
	ue = UE.objects.filter(semestre_id=id)

	if ue :
		ue.delete()

	matiere = Matiere.objects.filter(ue_id=id)

	if matiere :
		matiere.delete()

	semestre.delete()
	return render(request, 'contenu_html/supprsem.html', locals())

"""Cette vue permet de modifier un semestre"""
def modifierSemestre(request):
	if request.method == 'POST':
		if not request.session['sem']:
			Semestres = Semestre.objects.all()
			form = SelectSem(request.POST, semestres=Semestres)
			if form.is_valid() :
				id_sem = form.cleaned_data['select']
				request.session['id_sem'] = id_sem
				request.session['sem'] = True
			res = True
			s = get_object_or_404(Semestre, id=request.session['id_sem'])
			form = RenseignerSem(semestre=s)
		else:
			s = get_object_or_404(Semestre, id=request.session['id_sem'])
			form = RenseignerSem(request.POST, semestre=s)
			if form.is_valid() :
				semestre = get_object_or_404(Semestre, id=request.session['id_sem'])
				if form.cleaned_data['intitule']:
					semestre.intitule = form.cleaned_data['intitule']
				if form.cleaned_data['code_apogee']:
					semestre.code_apogee = form.cleaned_data['code_apogee']
				if form.cleaned_data['code_ppn']:
					semestre.code_apogee = form.cleaned_data['code_ppn']
				if form.cleaned_data['diplome']:
					semestre.diplome = form.cleaned_data['diplome']
				semestre.save()
				#request.session['mat'] = False
				res2=True
			else :
				print("ERREUR : MODIFIER Semestre : VIEW modifierSemestre : formulaire")
	else :
		Semestres = Semestre.objects.all()
		request.session['sem'] = False
		form = SelectSem(semestres=Semestres)
	return render(request, 'contenu_html/modifierSemestre.html', locals())


def ajouter_instance_semestre(request):
	if request.method == 'POST':
		form = InstanceSemestreForm(request.POST)
		if form.is_valid():

			annee = form.cleaned_data['annee']
			semestre = form.cleaned_data['semestre']

			# L'instance du semestre
			IS = InstanceSemestre(
					annee=annee,
					semestre = semestre,
			)

			IS.save()
			res = True
		else :
			print("ERREUR : AJOUTER IS : VIEW ajouter_instance_semestre : formulaire")
	else :
		form = InstanceSemestreForm()
	return render(request, 'contenu_html/ajouterInstanceSemestre.html', locals())


"""Cette vue permet de faire afficher les étudiants d'une Instance de semestre"""
def afficherInstanceSemestre(request):
	if request.method == 'POST':
		instanceSemestres = InstanceSemestre.objects.all()
		form = SelectInstanceSemestre(request.POST, instanceSemestres=instanceSemestres)
		if form.is_valid() :
			id_inst = form.cleaned_data['select']
			instanceSemestre = get_object_or_404(InstanceSemestre, id=id_inst)
			listeEtu = Appartient.objects.filter(instance_semestre=instanceSemestre)
			res = True
		else:
			print("ERREUR : Afficher promotion: VIEW afficher Promotion : formulaire")
	else:
		instanceSemestres = InstanceSemestre.objects.all()
		form = SelectInstanceSemestre(instanceSemestres=instanceSemestres)
	return render(request, 'contenu_html/afficherInstanceSemestre.html', locals())

"""Cette vue permet de faire evoluer les semestres instanciées"""
def faireEvoluerInstanceSemestre(request):
	if request.method == 'POST':
		if not request.session['inst']:
			instances = InstanceSemestre.objects.all()
			form = SelectInstanceSemestre(request.POST, instanceSemestres=instances)
			if form.is_valid() :
				id_instance = form.cleaned_data['select']
				request.session['id_instance'] = id_instance
				request.session['inst']=True
			instance = get_object_or_404(InstanceSemestre, id=request.session['id_instance'])
			lignes= Appartient.objects.filter(instance_semestre=instance).count()
			listeEvolution=[[""]* 4 for _ in range(lignes)]

			listeAppartient=Appartient.objects.filter(instance_semestre=instance)
			print(listeAppartient)
			i=0
			for ligne in listeAppartient:
				print(ligne)
				try:
					resSemestre= Resultat_Semestre.objects.get(etudiant=ligne.etudiant,instance_semestre=instance)
					listeEvolution[i][0]=ligne.etudiant.nom
					listeEvolution[i][1]=ligne.etudiant.prenom
					listeEvolution[i][2]=resSemestre.resultat
					listeEvolution[i][3]=ligne.etudiant.apogee
					i+=1
				except Resultat_Semestre.DoesNotExist:
					listeEvolution[i][0]=ligne.etudiant.nom
					listeEvolution[i][1]=ligne.etudiant.prenom
					listeEvolution[i][2]='Résultat inexistant'
					listeEvolution[i][3]=ligne.etudiant.apogee
					i+=1
					print('Erreur, cet etudiant n\'a pas de Resultat_Semestre')
			res = True
			request.session['listeEvolution'] = listeEvolution
			instances = InstanceSemestre.objects.all()
			form = EvolutionSemestreForm(listeAppartient=listeAppartient,instanceSemestres=instances)
			i=0
			for ligne in listeAppartient:
				listeEvolution[i][3] = str(form[str(ligne.etudiant.apogee)])
				i +=1
		else:
			instances = InstanceSemestre.objects.all()
			instance = get_object_or_404(InstanceSemestre, id=request.session['id_instance'])
			listeAppartient=Appartient.objects.filter(instance_semestre=instance)
			form = EvolutionSemestreForm(request.POST, listeAppartient=listeAppartient,instanceSemestres=instances)

			if form.is_valid() :
				if form.cleaned_data['select']:
						new_instance = form.cleaned_data['select']
						instance = get_object_or_404(InstanceSemestre, id=new_instance)
				for ligne in listeAppartient:
					if form.cleaned_data[str(ligne.etudiant.apogee)]:
						appartient = Appartient(
							instance_semestre = instance,
							etudiant = ligne.etudiant,
						)
						appartient.save()
				res2=True
			else:
				print("ERREUR : Afficher faire evoluer instance: VIEW faire evoluer instance : formulaire")
	else:
		instances = InstanceSemestre.objects.all()
		request.session['inst']=False
		form = SelectInstanceSemestre(instanceSemestres=instances)
	return render(request, 'contenu_html/faireEvoluerInstance.html',locals())

"""Cette vue permet d'afficher les étudiants présents dans un Semestre"""
def etudiants(request):
	ISemestres = InstanceSemestre.objects.all().filter(semestre__code_apogee="Semestre 1")
	App = Appartient.objects.all().filter(instance_semestre=ISemestres)
	return render(request, 'contenu_html/etudiants.html',locals())
