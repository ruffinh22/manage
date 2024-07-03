#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from Diplome.models import Diplome
from Annee.models import Annee
# Create your models here.


class Semestre(models.Model):
	code_ppn = models.CharField(max_length=30,null=False)
	code_apogee = models.CharField(max_length=30,null=False)
	intitule = models.CharField(max_length=30, null=False)
	diplome = models.ForeignKey(Diplome, null=True, on_delete=models.CASCADE)
	def __str__(self):
		return self.intitule

class InstanceSemestre(models.Model):
	annee = models.ForeignKey(Annee, null=False, on_delete=models.CASCADE)
	semestre = models.ForeignKey(Semestre, null=False, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.semestre)