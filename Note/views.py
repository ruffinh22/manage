#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from io import StringIO
from django import forms
from Note.forms import FileForm, SelectNote, RenseignerNote,CompleterResultat
from Etudiant.forms import SelectEtu
from UE.forms import SelectSemestre
from Etudiant.models import Etu,Appartient
from Note.models import Note,Resultat_Semestre,Resultat_UE
from Matiere.models import Matiere
from Semestre.models import Semestre,InstanceSemestre
from Semestre.forms import SelectInstanceSemestre
from Annee.models import Annee
from UE.models import UE
import csv
import datetime

"""Cette vue permet d'afficher les résultats jury pour un étudiant"""
def resultatJury(request):
	if request.method == 'POST':
			instances = InstanceSemestre.objects.all()
			form = SelectInstanceSemestre(request.POST, instanceSemestres=instances)

			if form.is_valid() :
				id_instance = form.cleaned_data['select']
				request.session['id_instance'] = id_instance
				request.session['instance'] = True
				res = True
				instance = InstanceSemestre.objects.get(id=id_instance)
				resultatsJury = Resultat_Semestre.objects.filter(instance_semestre=request.session['id_instance'])
			else :
				print("ERREUR : resultatJury : VIEW resultatJury : formulaire")	
	else :
		Etudiants = Etu.objects.all()
		request.session['etu'] = False
		instances = InstanceSemestre.objects.all()
		form = SelectInstanceSemestre(instanceSemestres=instances)
	return render(request, 'contenu_html/resultatJury.html', locals())






"""Cette vue permet de supprimer tous les étudiants"""
def suppall(request):
	Note.objects.all().delete()
	return listernotes(request)



"""Cette fonction permet d'insérer une virgule a un index donné"""
def insert_comma(string, index):
    return string[:index] + ',' + string[index:]

"""Cette fonction permet de traiter les notes d'un élève"""
def traitement_eleve(ligne,notes,code_eleve,diplome,ret_notes,ret_etu,ret_mat,ret_ue,ret_sem,compteur_eleve_error,nb_ligne,compteur_note_error,compteur_note,compteur_eleve):
	nb_elements_tab = len(ligne)
	apogee=ligne[0]
	nom=ligne[1]
	prenom=ligne[2]

	#Création de l'année 
	now = datetime.datetime.now()
	year = now.year
	yearMoins = year-1
	annee, cr = Annee.objects.get_or_create(intitule=str(yearMoins) +"-"+str(year))
	annee.save()

	try :
		etudiant = Etu.objects.get(apogee=apogee)
		if(etudiant):
			compteur_eleve = compteur_eleve+1
				
			print('etudiant')
			print(code_eleve[0],apogee,code_eleve[1],nom,code_eleve[2],prenom)
			print("Diplome : " + diplome)
		#Il faudra get l'élève ici avec son num apogée
		for i in range(3,nb_elements_tab):
			nb_ligne=nb_ligne+1
			#On ajoutera ici chaque note à l'étudiant
			#Le tableau notes contient le code de la note et ligne la note
			if ligne[i] == "":
				#Cas ou il n'y a pas de notes
				# print(notes[i],"null")
				note = "null"
			elif len(ligne[i]) == 5 and "," not in ligne[i]:
				#Cas ou la note fait 5 char de long ex :"12369"
				note = insert_comma(ligne[i],2)
				# print(notes[i],note)
			elif len(ligne[i]) == 4 and "," not in ligne[i]:
				#Cas ou la note fait 4 char de long ex :"8563"
				note = insert_comma(ligne[i],1)
				# print(notes[i],note)
			else:
				#Cas classique ex :""4,5""
				# print(notes[i],ligne[i])
				note = ligne[i]
				print('note')

			try :
				#si on lit un chaine contenant par "Semestre"	
				if "Semestre" in notes[i] :
					semestre_instance = InstanceSemestre.objects.get(semestre__code_ppn=notes[i])
					note = note.replace(",",".")
					print("NOTE",type(note),note)
					if type(note) is str and note == "null":
						note = 0
					else:
						note = float(note)
						

					try:
						ResSem = Resultat_Semestre.objects.get(
							etudiant = etudiant,
							instance_semestre = semestre_instance,
						)

						ResSem.note = note
						ResSem.save()
					except Resultat_Semestre.DoesNotExist :
						ResSem = Resultat_Semestre(
							etudiant = etudiant,
							instance_semestre = semestre_instance,
							note = note,
						)
						ResSem.save()

					
				#si on lit un chaine contenants par "UE"	
				elif "UE" in notes[i]:
					#on commence par récupérer l'ue à l'aide de son code 
					ue = UE.objects.get(code_ppn=notes[i])
					note = note.replace(",", ".")
					if type(note) is str and note == "null":
						note = 0
					else:
						note = float(note)
					#on peut maintenant récupérer toutes les informations 
					Res_Ue, create = Resultat_UE.objects.get_or_create(
						instance_semestre= semestre_instance,
						etudiant = etudiant,
						ue = ue,
						note= note#note qui sera modifiée dans une autre vue
					)
					if not create:     
						Res_Ue.note = note
						Res_Ue.save()
				else:	
					#on commence par créer la matière	
					matiere = Matiere.objects.get(code_ppn=notes[i])
					if note != "null":
						note = note.replace(",", ".")
						note = float(note)
						noteExiste = Note.objects.filter(etudiant=etudiant,matiere=matiere,instance_semestre=semestre_instance)

						if not noteExiste:
							n, created = Note.objects.get_or_create(valeur=note,etudiant=etudiant,matiere=matiere,instance_semestre=semestre_instance)
						
							if created==False:
									#print("La note",note,etudiant,matiere,"existait deja, elle n'a pas ete ajoutee")
									compteur_note_error = compteur_note_error + 1
									ret_notes.add("La note "+str(note)+" "+etudiant.nom+" "+matiere.intitule+" existait deja, elle n'a pas ete ajoutee")
							else:
									compteur_note = compteur_note +1
							n.save()
						else:
							noteExiste[0].valeur=note
							noteExiste[0].save()
							compteur_note_error = compteur_note_error + 1
			except Matiere.DoesNotExist :
				ret_mat.add("La matiere "+notes[i]+" n'existe pas")
			except Semestre.DoesNotExist :
				ret_sem.add("Le semestre "+notes[i]+" n'existe pas")
			except UE.DoesNotExist :
				ret_ue.add("L'UE "+notes[i]+" n'existe pas")
			except InstanceSemestre.DoesNotExist :
				ret_sem.add("L'instance de semestre "+notes[i]+" n'existe pas")
	except Etu.DoesNotExist :
		print("L'étudiant",nom,prenom,apogee,"n'existe pas")
		ret_etu.add("L'etudiant "+nom+" "+prenom+" "+str(apogee)+" n'existe pas")
		compteur_eleve_error=compteur_eleve_error+1
	return ret_notes,ret_etu,ret_mat,ret_ue,ret_sem,compteur_eleve_error,nb_ligne,compteur_note_error,compteur_note,compteur_eleve

# Create your views here.
"""Cette fonction permet d'importer via un formulaire un fichier CSV complet exporté par signature"""
def importer_csv(request):
	if request.method == "POST":
		form = FileForm(request.POST, request.FILES)
		if form.is_valid() :
			fichier = form.cleaned_data['fichier']
			
			import csv
			csvf = StringIO(fichier.read().decode('latin-1'))
			read = csv.reader(csvf, delimiter=',')

			nb_ligne = 0
			compteur_eleve=0
			compteur_eleve_error=0
			compteur_note=0
			compteur_note_error=0

			ret_notes = set()
			ret_etu = set()
			ret_mat = set()
			ret_ue = set()
			ret_sem = set()

			for row in read:
				if row[0].isdigit():
					ret_notes, ret_etu, ret_mat,ret_ue,ret_sem,compteur_eleve_error,nb_ligne,compteur_note_error,compteur_note,compteur_eleve = traitement_eleve(row,code_notes,code_eleve,diplome,ret_notes,ret_etu,ret_mat,ret_ue,ret_sem,compteur_eleve_error,nb_ligne,compteur_note_error,compteur_note,compteur_eleve)
				elif row[0] == "" and row[1] == "" and row[2] == "" :
					code_notes = row
				elif "GMP" in row[0]:
					diplome = row[0]
				else:
					code_eleve = row
	
			print(ret_notes,ret_etu,ret_mat)
			if len(ret_notes)==0 and len(ret_etu)==0 and len(ret_mat)==0:
    				perf=True
			else:  
					perf=False
					res = True
		else :
			print("ERREUR : IMPORT CSV : VIEW importer_csv : Formulaire")
	else :
		Resultat_UE.objects.all().delete()
		form = FileForm()
	return render(request, 'contenu_html/select_csv.html', locals())

"""Cette fonction permet de lister toutes les notes"""
def listernotes(request):
	notes = Note.objects.all().order_by('etudiant__nom')
	return render(request, 'contenu_html/listernotes.html',{'notes': notes})

"""Cette vue permet de supprimer une note"""
def supprnote(request, id):
	note = Note.objects.filter(id=id)
	note.delete()
	return render(request, 'contenu_html/supprnote.html', locals())

"""Cette vue permet de modifier une note"""
def modifierNote(request):
	if request.method == 'POST':
		if not request.session['note']:
			Notes = list(set(Note.objects.values_list('etudiant_id','etudiant__nom' )))
			form = SelectNote(request.POST, notes=Notes)
			if form.is_valid() :
				etudiant = form.cleaned_data['select']
				request.session['etudiant'] = etudiant
				request.session['note'] = True
			res = True
			NOTES = Note.objects.filter(etudiant_id=request.session['etudiant'])
			form = RenseignerNote(notes=NOTES)
	
		else:
			NOTES = Note.objects.filter(etudiant_id=request.session['etudiant'])
			form = RenseignerNote(request.POST, notes=NOTES)
			if form.is_valid() :
				for note in NOTES:
					note_temp = get_object_or_404(Note, id=note.id)
					if form.cleaned_data[note_temp.matiere.code_ppn]:
						note_temp.valeur = form.cleaned_data[note.matiere.code_ppn]
				note_temp.save()	
				res2=True
			else :
				print("ERREUR : MODIFIER Note : VIEW modifierNote : formulaire")	
	else :
		Notes = list(set(Note.objects.values_list('etudiant_id', 'etudiant__nom')))
		request.session['note'] = False
		form = SelectNote(notes=Notes)
	return render(request, 'contenu_html/modifierNote.html', locals())



def renseignerResultat(request):
	if request.method == 'POST':
		u = InstanceSemestre.objects.all()
		form = SelectInstanceSemestre(request.POST, instanceSemestres=u)
		if form.is_valid() :
			Isemes = form.cleaned_data['select']
			instancesemestre = InstanceSemestre.objects.get(id=Isemes)
		etus = Etu.objects.all()
		ues  = UE.objects.filter(semestre=instancesemestre.semestre)
		
		for etu in etus:
			moy = 0
			coeff = 0
			try:
				res = Resultat_Semestre.objects.get(etudiant=etu,instance_semestre = instancesemestre)
				
				if res is not None:
					notes = Note.objects.all().filter(etudiant=etu)
					
					for ue in ues:
						matieres = Matiere.objects.filter(ue=ue)
						for matiere in matieres :
							for note in notes :
								if note.matiere.intitule == matiere.intitule :
									note = Note.objects.get(etudiant=etu, matiere=matiere)
									moy += (note.valeur*matiere.coefficient)
									coeff += matiere.coefficient
				if coeff==0:
					coeff=1
				moyGcal = moy/coeff
				res = Resultat_Semestre.objects.get(etudiant=etu,instance_semestre = instancesemestre )
				moyG = res.note
				print('MOYG=', moyG)
				resultatSem = Resultat_Semestre.objects.get(etudiant=etu, instance_semestre=instancesemestre)
				barre = False
				print(instancesemestre.semestre)
				if instancesemestre.semestre.intitule == "Semestre 1":
					for ue in ues:
						res = Resultat_UE.objects.get(etudiant=etu,ue = ue)
						if res.note<8:
							barre=True
					if moyG>=10 and not barre:
						jury = "VAL"
					elif moyG>=8 and not barre:
						jury = "NATT"
					else:
						jury="NATB"
				
				else:
					if instancesemestre.semestre.intitule == "Semestre 2":
						semesPrec = InstanceSemestre.objects.get(semestre__intitule="Semestre 1")	
					elif instancesemestre.semestre.intitule == "Semestre 3":
						semesPrec =InstanceSemestre.objects.get(semestre__intitule="Semestre 2")
					elif instancesemestre.semestre.intitule == "Semestre 4":		
						semesPrec = InstanceSemestre.objects.get(semestre__intitule="Semestre 3")
					resSemPrec = Resultat_Semestre.objects.get(etudiant=etu, instance_semestre=semesPrec)
					moyGPrec = resSemPrec.note
					
					for ue in ues:
						res = Resultat_UE.objects.get(etudiant=etu,ue = ue)
						if res.note<8:
							barre=True
					
					if moyG>=10 and not barre and resSemPrec.resultat == "VAL":
						jury = "VAL"
					elif moyG>=10 and not barre and resSemPrec.resultat == "NATT" and (moyG+moyGPrec)>=20:
						jury = "ADAC"
					elif moyG>=10 and not barre and resSemPrec.resultat == "NATB" :
						jury = "AJPC"
					elif moyG>=8 and not barre and resSemPrec.resultat == "VAL" and (moyG+moyGPrec)>=10 :
						jury = "VALC"
					elif not barre:
						jury = "NATT"
					else:
						jury = "NATB"
					
					
				resultatSem.note_calc = moyGcal
				resultatSem.resultat = jury
				res=False
				resultatSem.save()
			except Resultat_Semestre.DoesNotExist:
				print("probleme")
	else :
		res=True
		u = InstanceSemestre.objects.all()
		form = SelectInstanceSemestre(instanceSemestres=u)
	return render(request, 'contenu_html/listerResultat.html',locals())

def completerResultat(request, id, Isemestre):
	if request.method == 'POST':
		try:
			etu=Etu.objects.get(id=id)
		except Etu.DoesNotExist:
			exist=False
		Instsem =InstanceSemestre.objects.get(id=Isemestre)
		if etu:
			exist=True

		resSem= Resultat_Semestre.objects.get(etudiant=etu,instance_semestre=Instsem)
		form = CompleterResultat(request.POST,res = resSem)
		if form.is_valid() :
			if form.cleaned_data['Resultat pre-jury']:
				resSem.resultat_pre_jury = form.cleaned_data['Resultat pre-jury']
			if form.cleaned_data['Resultat jury']:
				resSem.resultat_jury = form.cleaned_data['Resultat jury']
			resSem.save()
			res=True	
		else:
			print("ERREUR : Completer resultat: VIEW modifieResultats : formulaire")	
	else :
		try:
			etu=Etu.objects.get(id=id)
			Instsem =InstanceSemestre.objects.get(id=Isemestre)
			resSem= Resultat_Semestre.objects.get(etudiant=etu,instance_semestre=Instsem)
			form = CompleterResultat(res = resSem)
		except Etu.DoesNotExist:
			exist=False
	return render(request, 'contenu_html/completerResultat.html', locals())	
