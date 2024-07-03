from __future__ import unicode_literals
from django.db import models
from UE.models import UE 
from Semestre.models import Semestre
from Annee.models import Annee
# Create your models here.

class Matiere(models.Model):
	intitule = models.CharField(max_length=30,null=False)
	code_ppn = models.CharField(max_length=30,null=False)
	code_apogee = models.CharField(max_length=30,null=False)
	coefficient = models.FloatField(default=1.0)
	ue = models.ForeignKey('UE.ue', null=True , on_delete=models.CASCADE)	
	def __str__(self):
		return str(self.intitule).encode('utf8')
