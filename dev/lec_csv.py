#-*- coding: utf-8 -*-
import csv
import random
print("Lecture du Fichier CSV")

#cr = csv.reader(open("liste.csv","rb"))
ifile  = open('liste.csv', "r")
c = csv.writer(open("matière.csv", "wb"), delimiter=';')
read = csv.reader(ifile, delimiter=';')
for row in read:
	c.writerow([row[0],row[1],random.randint(0,20)])