from django import forms
from django.forms import ModelForm
from ..models import Category, User


class FilterOrderGroupsForm(forms.Form):
	date_gte = forms.DateField(label="From", required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type':"date", "class":"form-control"}))
	date_lte = forms.DateField(label="To", required=False, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type':"date", "class":"form-control"}))
	status = forms.IntegerField(label="Status", required=False,  widget=forms.Select(choices=[(0, 'ANY'), (1, 'OPEN'), (2, 'CLOSED')], attrs={"class":"form-control"}))
	waiter = forms.IntegerField(label="Waiter", required=False,  widget=forms.Select(choices=[(0, 'ANY'),], attrs={"class":"form-control"}))
	
	def __init__(self, v_model=False, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["waiter"].widget.choices += [(user.id, str(user)) for user in User.objects.exclude(profile=None).filter(groups__name="Waiter")]
		if v_model:
			self.add_v_models()

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

	def add_v_models(self):
		self.fields["date_gte"].widget.attrs["v-model"] = "dateGte"
		self.fields["date_lte"].widget.attrs["v-model"] = "dateLte"
		self.fields["waiter"].widget.attrs["v-model"] = "waiter"
		self.fields["status"].widget.attrs["v-model"] = "status"

