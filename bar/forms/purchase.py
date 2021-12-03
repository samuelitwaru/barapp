from django import forms
from django.forms import ModelForm
from ..models import Product



class FilterPurchasesForm(forms.Form):
	date_gte = forms.DateField(label="From", required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type':"date"}))
	date_lte = forms.DateField(label="To", required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type':"date"}))
	product = forms.IntegerField(label="Product", required=False,  widget=forms.Select)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["product"].widget.choices = [(product.id, product.name) for product in Product.objects.all()]