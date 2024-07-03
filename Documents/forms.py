#-*- coding: utf-8 -*-
from django import forms
from Diplome.models import Diplome



class DiplomeForm(forms.ModelForm):
	class Meta : 
		model = Diplome
		fields = '__all__'




