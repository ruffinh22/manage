#-*- coding: utf-8 -*-
from django import forms
from Annee.models import Annee



class AnneeForm(forms.ModelForm):
	class Meta : 
		model = Annee
		fields = '__all__'

class SelectAnn(forms.Form):
	def __init__(self,*args,**kwargs):
		annees = kwargs.pop('annees')
		super(SelectAnn,self).__init__(*args,**kwargs)
		AnnChoices = [(ann.id,ann.intitule) for ann in annees]
		self.fields['select'] = forms.ChoiceField(widget=forms.Select(), choices=AnnChoices)

class RenseignerAnn(forms.Form):
	
	def __init__(self,*args,**kwargs):
		ann = kwargs.pop('annee')
		super(RenseignerAnn,self).__init__(*args,**kwargs)

		if ann.intitule is None:
			self.fields['intitule']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['intitule'] = forms.CharField(max_length=100,required=False ,widget=forms.TextInput(attrs={'value': ann.intitule}))