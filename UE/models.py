from __future__ import unicode_literals

from django.db import models
from Semestre.models import Semestre 

# Create your models here.


class UE(models.Model):
	intitule = models.CharField(max_length=30,null=False)
	code_ppn = models.CharField(max_length=30,null=False)
	code_apogee = models.CharField(max_length=30,null=False)
	semestre = models.ForeignKey(Semestre, null=False, on_delete=models.CASCADE)
	coefficient = models.FloatField(null=False)
	def __str__(self):
		return self.code_ppn
    

