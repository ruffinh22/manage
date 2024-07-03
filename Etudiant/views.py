#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from Etudiant.models import Etu, Appartient
from Etudiant.forms import EtudiantForm, RenseignerEtu, SelectEtu
from Note.models import Note, Resultat_Semestre, Resultat_UE
from Note.forms import FileForm
from Semestre.models import Semestre, InstanceSemestre
from Semestre.forms import SelectInstanceSemestre
from UE.models import UE
from UE.forms import SelectSemestre
from Matiere.models import Matiere
import csv
from io import StringIO


from django.test.client import RequestFactory

"""Cette vue permet de lister les notes d'un étudiant"""
def listeretu(request, id):
    # On récupère l'étudiant
	etu = get_object_or_404(Etu, id=id)
	# On récupère les notes de l'étudiant en question
	notes = Note.objects.filter(etudiant__id=id)
	appartients = Appartient.objects.filter(etudiant__id=id)
	# On envoi vers la page
	return render(request, 'contenu_html/listeretu.html', locals())


"""Cette vue permet de supprimer un etudiant"""
def suppretu(request, id):
	appartients = Appartient.objects.filter(etudiant__id=id)
	resultat_semestres = Resultat_Semestre.objects.filter(etudiant__id=id)
	resultat_ues = Resultat_UE.objects.filter(etudiant__id=id)
	etu = get_object_or_404(Etu, id=id)
	notes = Note.objects.filter(etudiant__id=id)
	for resultat_semestre in resultat_semestres : 
			resultat_semestre.delete()
	for appartient in appartients:
			appartient.delete()
	for resultat_ue in resultat_ues:
			resultat_ue.delete()
	etu.delete()
	notes.delete()
	return render(request, 'contenu_html/suppretu.html',locals())

"""Cette vue permet de supprimer tous les étudiants"""
def suppall(request):
	Appartient.objects.all().delete()
	Resultat_Semestre.objects.all().delete()
	Resultat_UE.objects.all().delete()
	Note.objects.all().delete()
	Etu.objects.all().delete()
	return listeretus(request)

"""Cette vue permet d'ajouter un étudiant"""
def ajouterEtudiant(request):
	# Si la requete est un formulaire de type POST
	if request.method == 'POST':
    	# On récupère le formulaire 
		form = EtudiantForm(request.POST)
		if form.is_valid() :

			verif_Exist = Etu.objects.all().filter(apogee=form.cleaned_data['apogee'])
			# On vérifie que le numéro apogée n'existe pas déjà.
			if verif_Exist :
				print("Un étudiant avec ce numéro apogee existe déjà")
				exist = True

			else :
    			# On récupère les valeurs du formulaires
				nom = form.cleaned_data['nom']
				prenom = form.cleaned_data['prenom']
				apogee = form.cleaned_data['apogee']
				e = Etu(
						nom=nom,
						prenom=prenom,
						apogee=apogee,
			    )
				e.save()
				res = True
		else :
			print("ERREUR : AJOUTER Etudiant : VIEW ajouterEtudiant : formulaire")
	else :
		form = EtudiantForm() 
	return render(request, 'contenu_html/ajouterEtudiant.html', locals())

"""Cette vue permet de lister tous les étudiants"""
def listeretus(request):
	etus = Etu.objects.all()
	appartients = Appartient.objects.all()
	return render(request, 'contenu_html/listeretus.html',locals())

"""Cette vue permet de faire un affichage complet des notes d'un étudiant"""
def affichageComplet(request):
    # On regarde si la requete est un formulaire POST
	if request.method == 'POST':
		if not request.session['sem']:
			Etudiants = Etu.objects.all()
			form = SelectEtu(request.POST, etus=Etudiants)
			if form.is_valid() :
				id_etu = form.cleaned_data['select']
				request.session['id_etu'] = id_etu
				request.session['sem'] = True
			semestres = Semestre.objects.all()
			form = SelectSemestre(semestres=semestres)
		else:
			semestres = Semestre.objects.all()
			form = SelectSemestre(request.POST, semestres=semestres)
			if form.is_valid() :
				semestre = form.cleaned_data['select']
				semestre = Semestre.objects.get(id=semestre)
				if semestre:
					ues = UE.objects.all().filter(semestre=semestre)
					tab_matieres = []
					# Pour chaque UE on les ajoutes dans le tableau des matières
					for ue in ues :
						tab_matieres.append(Matiere.objects.all().filter(ue=ue))
					
					# On récupère les notes de l'étudiant courant
					notes = Note.objects.all().filter(etudiant__id=request.session['id_etu'])
					lignes = UE.objects.all().filter(semestre=semestre).count() + 2
					
					for matieres in tab_matieres :
						for matiere in matieres :
							lignes += 1
					
					colonnes = 4
					# On déclare les dimensions du tableau
					lst = [[""] * colonnes for _ in range(lignes)]
					lst[0][0] = "Elements"
					lst[0][1] = "Note"
					lst[0][2] = "Abscence"
					lst[0][3] = "Coefficient"
					lst[1][0] = semestre.code_ppn

					#Debut du contenu du tableau final
					i = 1
					coeff = 0
					moy = 0
					for matieres in tab_matieres :
						i += 1
						lst[i][0]=matieres[0].ue
						lst[i][3]= matieres[0].ue.coefficient 
						for matiere in matieres :
							i += 1
							lst[i][0]= matiere.intitule
							for note in notes :
								if note.matiere.intitule == matiere.intitule :
									lst[i][1] = note.valeur
									moy += (note.valeur*matiere.coefficient)
									coeff += matiere.coefficient
								
								# S'il n'y a pas de note on place un "-"
								if lst[i][1] == "" :
									lst[i][1] = "-"
								# Absence
								lst[i][2]= ""
								lst[i][3]= matiere.coefficient
					if coeff==0:
    						coeff=1
					lst[1][1] = moy/coeff
					res = True
					e = Etu.objects.get(id=request.session['id_etu'])
				else:
					semestre=False		
			else:
				print("ERREUR : AFFICHAGE Complte : VIEW affichageComplet : formulaire")
	else :
		semestre = False
		Etudiants = Etu.objects.all()
		request.session['sem'] = False
		form = SelectEtu(etus=Etudiants)
	return render(request, 'contenu_html/affichageComplet.html', locals())


"""Cette vue permet d'importer les étudiants"""
def importer_etu(request):
	if request.method == 'POST':
		if not request.session['instance']:
			instanceSemestres = InstanceSemestre.objects.all()
			form = SelectInstanceSemestre(request.POST, instanceSemestres=instanceSemestres)
			if form.is_valid() :
				id_instance = form.cleaned_data['select']
				request.session['id_instance'] = id_instance
				request.session['instance'] = True
			res = True
			instanceSemestre = get_object_or_404(InstanceSemestre, id=request.session['id_instance'])
			form = FileForm()
		else:
			instanceSemestre = get_object_or_404(InstanceSemestre, id=request.session['id_instance'])
			form = FileForm(request.POST, request.FILES)
			if form.is_valid() :
				fichier = form.cleaned_data['fichier']
	
				import csv
				csvf = StringIO(fichier.read().decode('latin-1'))
				read = csv.reader(csvf, delimiter=',')
				nb_etu = 0
				for row in read:
					if row[0].isdigit():
						nom = row[1]
						prenom = row[2]
						apogee = row[0]

						# On créé les nouveaux étudiants
						e, created = Etu.objects.get_or_create(
								nom=nom,
								prenom=prenom,
								apogee=apogee,
						)


						appartient, createdBis = Appartient.objects.get_or_create(
								etudiant=e,
								instance_semestre=instanceSemestre,
						)
						if created==True:
							nb_etu = nb_etu + 1
						e.save()
						appartient.save()
					else:
						code_eleve = row
				res2=True
			else :
				print("ERREUR : IMPORT CSV : VIEW importer_csv : Formulaire")
	else :
		instanceSemestres = InstanceSemestre.objects.all()
		if not instanceSemestres:
    			inst = False	
		else:
    			inst = True
		request.session['instance'] = False
		form = SelectInstanceSemestre(instanceSemestres=instanceSemestres)
	return render(request, 'contenu_html/importer_etudiant.html', locals())
	
		

"""Cette vue permet de renseigner le reste des informations"""
def complement_etu(request):
	if request.method == 'POST':
		if not request.session['etu']:
			Etudiants = Etu.objects.all()
			form = SelectEtu(request.POST, etus=Etudiants)
			if form.is_valid() :
				id_etu = form.cleaned_data['select']
				request.session['id_etu'] = id_etu
				request.session['etu'] = True
			res = True
			e = get_object_or_404(Etu, id=request.session['id_etu'])
			form = RenseignerEtu(etudiant=e)
		else:
			e = get_object_or_404(Etu, id=request.session['id_etu'])
			form = RenseignerEtu(request.POST, etudiant=e)
			if form.is_valid() :
				etudiant = get_object_or_404(Etu, id=request.session['id_etu'])
				if form.cleaned_data['nom']:
					etudiant.nom = form.cleaned_data['nom']
				if form.cleaned_data['prenom']:
					etudiant.prenom = form.cleaned_data['prenom']
				if form.cleaned_data['apogee']:
					etudiant.apogee = form.cleaned_data['apogee']
				if form.cleaned_data['date_naissance']:
					etudiant.date_naissance = form.cleaned_data['date_naissance']
				if form.cleaned_data['sexe']:
					etudiant.sexe = form.cleaned_data['sexe']
				if form.cleaned_data['adresse']:
					etudiant.adresse = form.cleaned_data['adresse']
				if form.cleaned_data['ine']:
					etudiant.ine = form.cleaned_data['ine']
				if form.cleaned_data['adresse_parents']:
					etudiant.adresse_parents = form.cleaned_data['adresse_parents']
				if form.cleaned_data['tel']:
					etudiant.tel = form.cleaned_data['tel']
				if form.cleaned_data['tel_par']:
					etudiant.tel_par = form.cleaned_data['tel_par']
				if form.cleaned_data['lieu_naissance']:
					etudiant.lieu_naissance = form.cleaned_data['lieu_naissance']
				if form.cleaned_data['nationalite']:
					etudiant.nationalite = form.cleaned_data['nationalite']
				if form.cleaned_data['situation_familiale']:
					etudiant.situation_familiale = form.cleaned_data['situation_familiale']
				if form.cleaned_data['situation_militaire']:
					etudiant.situation_militaire = form.cleaned_data['situation_militaire']
				if form.cleaned_data['cate_socio_pro_chef_famille']:
					etudiant.cate_socio_pro_chef_famille = form.cleaned_data['cate_socio_pro_chef_famille']
				if form.cleaned_data['cate_socio_pro_autre_parent']:
					etudiant.cate_socio_pro_autre_parent = form.cleaned_data['cate_socio_pro_autre_parent']
				if form.cleaned_data['aide_financiere']:
					etudiant.aide_financiere = form.cleaned_data['aide_financiere']
				if form.cleaned_data['bourse']:
					etudiant.bourse = form.cleaned_data['bourse']
				etudiant.save()	
				request.session['mat'] = False
				res2=True
			else :
				print("ERREUR : MODIFIER Etudiant : VIEW complement_etu : formulaire")	
	else :
		Etudiants = Etu.objects.all()
		request.session['etu'] = False
		form = SelectEtu(etus=Etudiants)
	return render(request, 'contenu_html/complement_etu.html', locals())

