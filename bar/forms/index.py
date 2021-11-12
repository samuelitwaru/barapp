from django import forms
from ..models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput)


class SetPasswordForm(forms.Form):
	password = forms.CharField(label="Password", widget=forms.PasswordInput)
	confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")
		if password != confirm_password:
			raise forms.ValidationError("Passwords do not match!")


class ForgotPasswordForm(forms.Form):
	email = forms.EmailField(label="Email")

	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get("email")
		user = User.objects.filter(username=email).first()
		if not user:
			raise forms.ValidationError("There is no user registered with this email!")
		cleaned_data["email"] = user



class UpdateUserPasswordForm(forms.Form):
    current_password = forms.CharField(label="Current Password", widget=forms.PasswordInput)
    new_password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

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


class AuthenticationForm(forms.Form):
	redirect_url = forms.CharField(widget=forms.HiddenInput())
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"p-1", 'placeholder':'Enter your password...'}))