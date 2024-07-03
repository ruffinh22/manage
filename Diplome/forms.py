#-*- coding: utf-8 -*-
from django import forms
from Diplome.models import Diplome
from Annee.models import Annee

class DiplomeForm(forms.ModelForm):
	class Meta : 
		model = Diplome
		fields = '__all__'

class DiplomeFormCreation(forms.Form):
	def __init__(self,*args,**kwargs):
		monAnnee = kwargs.pop('monAnnee')
		super(DiplomeFormCreation,self).__init__(*args,**kwargs)
		self.fields['monAnnee'] = forms.ChoiceField(label="Diplome",choices=[(x.plug_ip, x.nom) for x in Diplome.objects.filter(annee = monAnnee)])

class SelectDip(forms.Form):
	def __init__(self,*args,**kwargs):
		diplomes = kwargs.pop('diplomes')
		super(SelectDip,self).__init__(*args,**kwargs)
		DipChoices = [(dip.id,dip.intitule) for dip in diplomes]
		self.fields['select'] = forms.ChoiceField(widget=forms.Select(), choices=DipChoices)

class RenseignerDip(forms.Form):
	
	def __init__(self,*args,**kwargs):
		dip = kwargs.pop('diplome')
		super(RenseignerDip,self).__init__(*args,**kwargs)

		if dip.intitule is None:
			self.fields['intitule']  = forms.CharField(max_length=100,required=False)
		else:
			self.fields['intitule'] = forms.CharField(max_length=100,required=False ,widget=forms.TextInput(attrs={'value': dip.intitule}))

	