from django.forms import ModelForm
from diriwa.models import *

class RegionForm(ModelForm):
	class Meta:
		model = Region
		

class SectionForm(ModelForm):
	class Meta:
		model = Section
		exclude = ('region', )

