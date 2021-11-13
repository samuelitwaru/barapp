from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Order, Profile
from ..forms import UpdateProfileForm, UpdateUserForm, UpdatePasswordForm, UpdateUserPermissionsForm, UpdateUserPasswordForm
from ..utils import split_telephone


@login_required
def get_profiles(request):
	profiles = Profile.objects.all()
	context = {
		"profiles": profiles
	}
	return render(request, 'profile/profiles.html', context)


@login_required
def get_profile(request, id):
	profile = Profile.objects.filter(id=id).first()
	user = profile.user
	tel_code, telephone = split_telephone(profile.telephone)
	update_user_password_form = UpdateUserPasswordForm()
	update_user_form = UpdateUserForm(data={"name": profile.name, "email":profile.email, "tel_code":tel_code, "telephone":telephone, "is_active":profile.user.is_active}, profile=profile)
	update_user_permissions_form = UpdateUserPermissionsForm({
			"can_make_orders": user.has_perm('bar.can_make_orders'),
			"can_mark_orders_as_ready": user.has_perm('bar.can_mark_orders_as_ready'),
			"can_mark_orders_as_served": user.has_perm('bar.can_mark_orders_as_served'),
		})
	context = {
		"profile": profile,
		"update_user_form": update_user_form,
		"update_user_password_form": update_user_password_form,
		"update_user_permissions_form": update_user_permissions_form,
	}
	return render(request, 'profile/profile.html', context)


@login_required
def get_current_user_profile(request):
	profile = request.user.profile
	tel_code, telephone = split_telephone(profile.telephone)
	update_profile_form = UpdateProfileForm(data={"name": profile.name, "email":profile.email, "tel_code":tel_code, "telephone":telephone}, profile=profile)
	update_password_form = UpdatePasswordForm()
	tab = request.GET.get("tab", 'profile')
	context = {
		"tab": tab,
		"update_profile_form": update_profile_form,
		"update_password_form": update_password_form
	}
	return render(request, 'pages/profile.html', context)


@login_required
def update_current_user_profile(request):
	user = request.user
	profile = user.profile
	update_profile_form = UpdateProfileForm(data=request.POST, profile=profile)
	if request.method == "POST" and update_profile_form.is_valid():
		data = update_profile_form.cleaned_data
		profile.name = data["name"]
		profile.email = data["email"]
		profile.telephone = data["telephone"]
		user.email = data["email"]
		user.username = data["email"]
		profile.save()
		user.save()
		messages.success(request, f"Profile updated.")
		return redirect('bar:get_current_user_profile')

	update_password_form = UpdatePasswordForm()
	context = {
		"tab": 'profile',
		"update_profile_form": update_profile_form,
		"update_password_form": update_password_form
	}
	return render(request, 'pages/profile.html', context)


@login_required
def update_current_user_password(request):
	user = request.user
	update_password_form = UpdatePasswordForm(data=request.POST, user=user)
	if request.method == "POST" and update_password_form.is_valid():
		data = update_password_form.cleaned_data
		user.set_password(data["new_password"])
		user.save()
		messages.success(request, f"Password updated.")
		return redirect(reverse('bar:get_current_user_profile') + '?tab=password')

	profile = user.profile
	tel_code, telephone = split_telephone(profile.telephone)
	update_profile_form = UpdateProfileForm(data={"name": profile.name, "email":profile.email, "tel_code":tel_code, "telephone":telephone}, profile=profile)
	context = {
		"tab": 'password',
		"update_profile_form": update_profile_form,
		"update_password_form": update_password_form
	}
	return render(request, 'pages/profile.html', context)