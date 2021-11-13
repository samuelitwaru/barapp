from django import forms
from ..models import User, Profile
from django.contrib.auth import authenticate
from ..utils import join_telephone, TEL_CODES


class UpdateProfileForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
	email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control"}))
	tel_code = forms.CharField(required=False, widget=forms.Select(choices=TEL_CODES, attrs={"class":"form-control"}))
	telephone = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"placeholder":"eg 781567890", "class":"form-control"}))


	def __init__(self, profile, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.profile = profile
		self.user = self.profile.user
		# self.fields["name"].default = self.profile.name

	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get("email")
		tel_code = cleaned_data.get("tel_code")
		telephone = cleaned_data.get("telephone")

		if User.objects.exclude(username=self.user.username).filter(username=email).count():
			raise forms.ValidationError("A user with this email address already exists.")

		if telephone and tel_code:
			cleaned_data["telephone"] = join_telephone(tel_code, telephone)
		else:
			cleaned_data["telephone"] = None	
		telephone = cleaned_data.get("telephone")

		if telephone and Profile.objects.exclude(telephone=self.profile.telephone).filter(telephone=telephone).count():
			raise forms.ValidationError("A user with this telephone number already exists.")


class UpdatePasswordForm(forms.Form):
	current_password = forms.CharField(label="Current Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
	new_password = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))
	confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

	def __init__(self, user=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user = user

	def clean(self):
		cleaned_data = super().clean()
		current_password = cleaned_data.get("current_password")
		new_password = cleaned_data.get("new_password")
		confirm_password = cleaned_data.get("confirm_password")
		user = authenticate(username=self.user.username, password=current_password)
		if not user:
			self.add_error('current_password', "Incorrect Password!")
		if new_password != confirm_password:
			self.add_error('confirm_password', "Passwords do not match!")