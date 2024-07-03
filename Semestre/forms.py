#-*- coding: utf-8 -*-
from django import forms
from Semestre.models import Semestre,InstanceSemestre
from Diplome.models import Diplome

class InstanceSemestreForm(forms.ModelForm):
	class Meta :
		model = InstanceSemestre
		fields = '__all__'

class SelectInstanceSemestre(forms.Form):
	def __init__(self,*args,**kwargs):
		instanceSemestres = kwargs.pop('instanceSemestres')
		super(SelectInstanceSemestre,self).__init__(*args,**kwargs)
		ISChoice = [(instanceSemestre.id,str(instanceSemestre.semestre) + " de l'année " + str(instanceSemestre.annee)) for instanceSemestre in instanceSemestres]
		self.fields['select'] = forms.ChoiceField(widget=forms.Select(), choices=ISChoice, label="Semestre courant")

class EvolutionSemestreForm(forms.Form):
	def __init__(self,*args,**kwargs):
		Liste = kwargs.pop('listeAppartient')
		instances = kwargs.pop('instanceSemestres')
		super(EvolutionSemestreForm,self).__init__(*args,**kwargs)
		for ligne in Liste:
			self.fields[str(ligne.etudiant.apogee)] = forms.BooleanField(required=False)
		ISChoice = [(instanceSemestre.id,str(instanceSemestre.semestre) + " de l'année " + str(instanceSemestre.annee)) for instanceSemestre in instances]
		self.fields['select'] = forms.ChoiceField(widget=forms.Select(), choices=ISChoice)



class SemestreForm(forms.Form):
	def __init__(self,*args,**kwargs):

		SEMESTRE = (
			('Semestre 1','Semestre 1'),
			('Semestre 2','Semestre 2'),
			('Semestre 3','Semestre 3'),	
			('Semestre 4','Semestre 4')
		)
		diplomes = kwargs.pop('diplomes')
		super(SemestreForm,self).__init__(*args,**kwargs)
		DIPLOME = [(dip.id,dip.intitule) for dip in diplomes]
		print(DIPLOME)
		self.fields['code_ppn'] = forms.CharField(label='Code PPN')
		self.fields['code_apogee'] = forms.CharField(label='Code Apogée')
		self.fields['diplome'] = forms.ChoiceField(widget=forms.Select(), choices=DIPLOME)
		self.fields['intitule'] = forms.ChoiceField(widget=forms.Select(), choices=SEMESTRE)


class SelectSem(forms.Form):
	def __init__(self,*args,**kwargs):
		semestres = kwargs.pop('semestres')
		super(SelectSem,self).__init__(*args,**kwargs)
		SemChoices = [(sem.id,sem.code_ppn) for sem in semestres]
		self.fields['select'] = forms.ChoiceField(widget=forms.Select(), choices=SemChoices)

class RenseignerSem(forms.Form):

	def __init__(self,*args,**kwargs):
		sem = kwargs.pop('semestre')
		super(RenseignerSem,self).__init__(*args,**kwargs)

		if sem.intitule is None:
			self.fields['intitule']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['intitule'] = forms.CharField(max_length=100,required=False ,widget=forms.TextInput(attrs={'value': sem.intitule}))

		if sem.code_apogee is None:
			self.fields['code_apogee']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['code_apogee'] = forms.CharField(max_length=100,required=False ,widget=forms.TextInput(attrs={'value': sem.code_apogee}))

		if sem.code_ppn is None:
			self.fields['code_ppn']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['code_ppn'] = forms.CharField(max_length=100,required=False ,widget=forms.TextInput(attrs={'value': sem.code_ppn}))

		if sem.diplome is None:
			self.fields['diplome'] = forms.ModelChoiceField(queryset=Diplome.objects.all(),required=False)
		else:
			self.fields['diplome']  = forms.ModelChoiceField(queryset=Diplome.objects.all().exclude(id=sem.diplome.id), empty_label=sem.diplome,required=False)
