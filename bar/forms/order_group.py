from django import forms
from django.forms import ModelForm
from ..models import Category


class FilterOrderGroupsForm(forms.Form):
	date_gte = forms.DateField(label="From", required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type':"date"}))
	date_lte = forms.DateField(label="To", required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type':"date"}))
	status = forms.IntegerField(label="Status", required=False,  widget=forms.Select(choices=[(0, 'ANY'), (1, 'OPEN'), (2, 'CLOSED')]))
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super().clean()
		date_lte = cleaned_data.get("date_lte")
		date_gte = cleaned_data.get("date_gte")
		status = cleaned_data.get("status")
		if status:
			if status == 1:
				status = False
			else:
				status = True
			self.cleaned_data["status"] = status

