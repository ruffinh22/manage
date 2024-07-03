#-*- coding: utf-8 -*-
from django import forms
from UE.models import UE
from Matiere.models import Matiere



class MatiereForm(forms.ModelForm):
	class Meta : 
		model = Matiere
		fields = '__all__'
		exclude = ['ue']


class SelectUE(forms.Form):
	
	def __init__(self,*args,**kwargs):
		unites = kwargs.pop('ues')
		super(SelectUE,self).__init__(*args,**kwargs)
		UeChoices = [(ue.id,ue.code_ppn) for ue in unites]
		self.fields['select'] = forms.ChoiceField(widget=forms.Select(), choices=UeChoices)

class SelectMat(forms.Form):
	def __init__(self,*args,**kwargs):
		matieres = kwargs.pop('matieres')
		super(SelectMat,self).__init__(*args,**kwargs)
		MatChoices = [(mat.id,mat.intitule) for mat in matieres]
		self.fields['select'] = forms.ChoiceField(widget=forms.Select(), choices=MatChoices)

class RenseignerMat(forms.Form):
	# class Meta : 
	#  	model = Etu
	# 	fields = '__all__'
	#  	exclude = ['nom','prenom']
	def __init__(self,*args,**kwargs):
		mat = kwargs.pop('matiere')
		super(RenseignerMat,self).__init__(*args,**kwargs)

		if mat.intitule is None:
			self.fields['intitule']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['intitule'] = forms.CharField(max_length=100,required=False ,widget=forms.TextInput(attrs={'value': mat.intitule}))


		if mat.code_apogee is None:
			self.fields['code_apogee']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['code_apogee'] = forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs={'value': mat.code_apogee}))

		if mat.code_ppn is None:
			self.fields['code_ppn']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['code_ppn'] = forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs={'value': mat.code_ppn}))

		if mat.coefficient is None:
			self.fields['coefficient']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['coefficient'] = forms.CharField(max_length=100,required=False, widget=forms.TextInput(attrs={'value': mat.coefficient}))

		if mat.ue is None:
			self.fields['unite'] = forms.ModelChoiceField(queryset=UE.objects.all(),required=False)
		else:
			self.fields['unite']  = forms.ModelChoiceField(queryset=UE.objects.all().exclude(id=mat.ue.id), empty_label=mat.ue,required=False)




