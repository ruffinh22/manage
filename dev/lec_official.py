#-*- coding: utf-8 -*-
import csv
import random
print("Lecture du Fichier CSV")

#cr = csv.reader(open("liste.csv","rb"))
ifile  = open('liste.csv', "r")
c = csv.writer(open("matière.csv", "wb"), delimiter=';')
read = csv.reader(ifile, delimiter=';')
i = 0
for row in read:
	i += 1

	if(i<=4):
		if(row):
			print(row[0])
			if i == 1:
				intitule_matiere = row[0].split(": ")
				intitule_matiere = intitule_matiere[1]
			if i == 2:
				date = row[0].split(": ")
				date = date[1]
			if i == 3:
				data = row[0].split(": ")
				enseignant = data[1].split(" ")
				prenom = enseignant[0]
				nom = enseignant[1]
	else:
		print(row[0])
		print(row[1])
		print(row[2])
	#c.writerow([row[0],row[1],random.randint(0,20)])
print(intitule_matiere)
print(date)
print(prenom)
print(nom)