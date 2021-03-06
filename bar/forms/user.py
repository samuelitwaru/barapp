import os
from random import randint
from django import forms
from django.contrib.auth.models import Group
from .profile import UpdateProfileForm
from ..utils import TEL_CODES, join_telephone
from ..models import User, Profile



class CreateUserForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
	email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control"}))
	tel_code = forms.CharField(required=False, widget=forms.Select(choices=TEL_CODES, attrs={"class":"form-control"}))
	telephone = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"placeholder":"eg 781567890", "class":"form-control"}))
	user_group = forms.ChoiceField(widget=forms.RadioSelect(attrs={"v-model":"userGroup"}))
	password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control", ":required":"!userGroup==3"}))
	confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={"class":"form-control", ":required":"!userGroup==3"}))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["user_group"].choices = [(group.id, group.name) for group in Group.objects.all()]
		is_waiter = self.data.get("user_group") == '3'
		if is_waiter:
			self.fields["email"].required = False
			self.fields["password"].required = False
			self.fields["confirm_password"].required = False

	def clean(self):
		cleaned_data = super().clean()
		is_waiter = int(cleaned_data.get("user_group")) == 3
		name = cleaned_data.get("name")

		if not is_waiter:
			password = cleaned_data.get("password")
			confirm_password = cleaned_data.get("confirm_password")
			if password != confirm_password:
				self.add_error('confirm_password', "Passwords do not match!")
		else:
			cleaned_data["email"] = f"{name.replace(' ','').lower()}{randint(0,9)}"
			cleaned_data["password"] = os.environ["DEFAULT_PASSWORD"]

		email = cleaned_data.get("email")
		if User.objects.filter(username=email).count():
			self.add_error('email', "A user with this email address already exists.")

		tel_code = cleaned_data.get("tel_code")
		telephone = cleaned_data.get("telephone")
		if telephone and tel_code:
			cleaned_data["telephone"] = join_telephone(tel_code, telephone)
		else:
			cleaned_data["telephone"] = None	
		telephone = cleaned_data.get("telephone")

		if telephone and Profile.objects.filter(telephone=telephone).count():
			self.add_error('telephone', "A user with this telephone number already exists.")


class UpdateWaiterForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
	tel_code = forms.CharField(required=False, widget=forms.Select(choices=TEL_CODES, attrs={"class":"form-control"}))
	telephone = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"placeholder":"eg 781567890", "class":"form-control"}))
	is_active = forms.BooleanField(label="User is ACTIVE", required=False)
	# user_group = forms.ChoiceField(widget=forms.RadioSelect(attrs={"v-model":"userGroup"}))

	def __init__(self, profile, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super().clean()
		tel_code = cleaned_data.get("tel_code")
		telephone = cleaned_data.get("telephone")
		if telephone and tel_code:
			cleaned_data["telephone"] = join_telephone(tel_code, telephone)
		else:
			cleaned_data["telephone"] = None	


class UpdateUserForm(UpdateWaiterForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control"}))

	def __init__(self, profile, *args, **kwargs):
		super().__init__(profile, *args, **kwargs)





class UpdateUserPasswordForm(forms.Form):
	new_password = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
	confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

	def clean(self):
		cleaned_data = super().clean()
		new_password = cleaned_data.get("new_password")
		confirm_password = cleaned_data.get("confirm_password")
      
		if new_password != confirm_password:
			self.add_error('confirm_password', "Passwords do not match!")


class UpdateUserPermissionsForm(forms.Form):
	can_make_orders = forms.BooleanField(label="User can MAKE orders", required=False)
	can_mark_orders_as_ready = forms.BooleanField(label="User can mark orders as READY", required=False)
	can_mark_orders_as_served = forms.BooleanField(label="User can mark orders as PAID", required=False)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)