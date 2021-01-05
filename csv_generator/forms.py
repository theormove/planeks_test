from django import forms
from .models import DataSchemaColumn


class DataSchemaColumnForm(forms.ModelForm):

	class Meta:
		model = DataSchemaColumn
		fields = ('name','column_type','order')		