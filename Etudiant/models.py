#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from Annee.models import Annee
from Semestre.models import Semestre, InstanceSemestre

# Create your models here.
class Etu(models.Model):
	nom = models.CharField(max_length=30, null=False)
	prenom = models.CharField(max_length=30, null=False)
	apogee = models.IntegerField(null=True)
	date_naissance = models.CharField(max_length=100,null=True)
	sexe = models.CharField(max_length=1, null=True)
	adresse = models.CharField(max_length=100, null=True)
	ine = models.CharField(max_length=100, null=True)
	adresse_parents = models.CharField(max_length=100, null=True)
	tel = models.IntegerField(null=True)
	tel_par = models.IntegerField(null=True)
	lieu_naissance = models.CharField(max_length=100, null=True)
	nationalite = models.CharField(max_length=100, null=True)
	situation_familiale = models.CharField(max_length=100, null=True)
	situation_militaire = models.CharField(max_length=100, null=True)
	cate_socio_pro_chef_famille = models.CharField(max_length=100, null=True)
	cate_socio_pro_autre_parent = models.CharField(max_length=100, null=True)
	aide_financiere = models.CharField(max_length=100, null=True)
	bourse = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.nom

class Appartient(models.Model):
	instance_semestre = models.ForeignKey(InstanceSemestre, null=False, on_delete=models.CASCADE)	
	etudiant = models.ForeignKey(Etu, null=False, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.etudiant).encode('utf-8')