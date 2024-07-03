#-*- coding: utf-8 -*-
import csv

"""Cette fonction permet d'insérer une virgule a un indice donné"""
def insert_comma(string, index):
    return string[:index] + ',' + string[index:]

"""Cette fonction permet de traiter les notes d'un élève"""
def traitement_eleve(ligne,notes,code_eleve,diplome):
	nb_elements_tab = len(ligne)
	apogee=ligne[0]
	nom=ligne[1]
	prenom=ligne[2]
	print(code_eleve[0],apogee,code_eleve[1],nom,code_eleve[2],prenom)
	print("Diplome : " + diplome)
	#Il faudra get l'élève ici avec son num apogée
	for i in range(3,nb_elements_tab):
		#On ajoutera ici chaque note à l'étudiant
		#Le tableau notes contient le code de la note et ligne la note
		if ligne[i] == "":
			#Cas ou il n'y a pas de notes
			print(notes[i],"null")
		elif len(ligne[i]) == 5 and "," not in ligne[i]:
			#Cas ou la note fait 5 char de long ex :"12369"
			note = insert_comma(ligne[i],2)
			print(notes[i],note)
		elif len(ligne[i]) == 4 and "," not in ligne[i]:
			#Cas ou la note fait 4 char de long ex :"8563"
			note = insert_comma(ligne[i],1)
			print(notes[i],note)
		else:
			#Cas classique ex :""4,5""
			print(notes[i],ligne[i])
	print()

ifile  = open('S1_2016_modif.csv', "r")
read = csv.reader(ifile, delimiter=',')
for row in read:
	if row[0].isdigit():
		traitement_eleve(row,code_notes,code_eleve,diplome)
	elif "Bilan" in row[0]:
		print(row[0])
	elif row[0] == "" and row[1] == "" and row[2] == "" :
		code_notes = row
	elif "GMP" in row[0]:
		diplome = row[0]
	else:
		code_eleve = row