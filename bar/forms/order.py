from django import forms
from django.forms import ModelForm
from ..models import Category, User, Product


class FilterOrdersForm(forms.Form):
	date_gte = forms.DateField(label="From", required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type':"date", "class":"form-control"}))
	date_lte = forms.DateField(label="To", required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type':"date", "class":"form-control"}))
	product = forms.IntegerField(label="Product", required=False,  widget=forms.Select(choices=[(0, "ANY")], attrs={'type':"date", "class":"form-control"}))
	
	def __init__(self, v_model=False, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["product"].widget.choices += [(product.id, product.name) for product in Product.objects.all()]
		
