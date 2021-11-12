from django import forms
from ..models import User
from django.contrib.auth import authenticate


class CreateMetricSystemForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))