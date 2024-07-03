#-*- coding: utf-8 -*-
from django import forms
from UE.models import UE
from Semestre.models import Semestre


class UEForm(forms.ModelForm):
	class Meta : 
		model = UE
		fields = '__all__'
		exclude = ['semestre']


class SelectSemestre(forms.Form):	
	def __init__(self,*args,**kwargs):
		semestre = kwargs.pop('semestres')
		super(SelectSemestre,self).__init__(*args,**kwargs)
		SemChoices = [(sem.id,sem.code_ppn) for sem in semestre]
		self.fields['select'] = forms.ChoiceField(label = "Choix du Semestre", widget=forms.Select(), choices=SemChoices)

class SelectUE(forms.Form):
	def __init__(self,*args,**kwargs):
		unites = kwargs.pop('ues')
		super(SelectUE,self).__init__(*args,**kwargs)
		UeChoices = [(ue.id,ue.code_ppn) for ue in unites]
		self.fields['select'] = forms.ChoiceField(widget=forms.Select(), choices=UeChoices)

class RenseignerUe(forms.Form):
	# class Meta : 
	#  	model = Etu
	# 	fields = '__all__'
	#  	exclude = ['nom','prenom']
	def __init__(self,*args,**kwargs):
		ue = kwargs.pop('ue')
		super(RenseignerUe,self).__init__(*args,**kwargs)

		if ue.intitule is None:
			self.fields['intitule']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['intitule'] = forms.CharField(max_length=100,required=False ,widget=forms.TextInput(attrs={'value': ue.intitule}))

		if ue.coefficient is None:
			self.fields['coefficient']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['coefficient'] = forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs={'value': ue.coefficient}))

		if ue.code_ppn is None:
			self.fields['code_ppn']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['code_ppn'] = forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs={'value': ue.code_ppn}))

		if ue.code_apogee is None:
			self.fields['code_apogee']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['code_apogee'] = forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs={'value': ue.code_apogee}))

		
		if ue.semestre is None:
			self.fields['semestre'] = forms.ModelChoiceField(queryset=Semestre.objects.all(),required=False)
		else:
			self.fields['semestre']  = forms.ModelChoiceField(queryset=Semestre.objects.all().exclude(id=ue.semestre.id), empty_label=ue.semestre,required=False)
