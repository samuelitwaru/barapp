from django import forms
from .profile import UpdateProfileForm
from ..utils import TEL_CODES, join_telephone
from ..models import User, Profile



class CreateUserForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
	email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control"}))
	tel_code = forms.CharField(required=False, widget=forms.Select(choices=TEL_CODES, attrs={"class":"form-control"}))
	telephone = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder":"eg 781567890", "type":"tel", "class":"form-control"}))

	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get("email")
		tel_code = cleaned_data.get("tel_code")
		telephone = cleaned_data.get("telephone")

		if User.objects.filter(username=email).count():
			self.add_error('email', "A user with this email address already exists.")

		if telephone and tel_code:
			cleaned_data["telephone"] = join_telephone(tel_code, telephone)
		else:
			cleaned_data["telephone"] = None	
		telephone = cleaned_data.get("telephone")

		if telephone and Profile.objects.filter(telephone=telephone).count():
			self.add_error('telephone', "A user with this telephone number already exists.")


class UpdateUserForm(UpdateProfileForm):
	is_active = forms.BooleanField(label="User is ACTIVE", required=False)


class UpdateUserPermissionsForm(forms.Form):
	can_make_orders = forms.BooleanField(label="User can MAKE orders", required=False)
	can_mark_orders_as_ready = forms.BooleanField(label="User can mark orders as READY", required=False)
	can_mark_orders_as_served = forms.BooleanField(label="User can mark orders as SERVED", required=False)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)