from django.views.generic import TemplateView, DetailView
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect 
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from ..models import User, Profile
from ..forms import UpdateUserPermissionsForm, UpdateUserForm, UpdateWaiterForm, CreateUserForm, UpdateUserPasswordForm
from ..decorators import *


@groups_required("Admin")
@login_required
def create_user(request):
	create_user_form = CreateUserForm()
	if request.method=="POST":
		create_user_form = CreateUserForm(request.POST)
		if create_user_form.is_valid():
			data = create_user_form.cleaned_data
			group = Group.objects.get(id=data['user_group'])
			user = User.objects.create(username=data["email"], email=data["email"])
			user.set_password(data["password"])
			user.groups.set([group])
			user.save()
			profile = Profile.objects.create(name=data["name"], email=data["email"], telephone=data["telephone"], user=user)
			messages.success(request, "User created")
			return redirect('bar:update_user', id=user.id)

	context = {
		"create_user_form": create_user_form
	}
	return render(request, 'profile/create-profile.html', context)


@groups_required("Admin")
@login_required
def update_user(request, id):
	user = User.objects.filter(id=id).first()
	profile = user.profile
	if "Waiter" in profile.roles():
		update_user_form = UpdateWaiterForm(data=request.POST, profile=profile)
	else:
		update_user_form = UpdateUserForm(data=request.POST, profile=profile)
	if request.method == "POST" and update_user_form.is_valid():
		data = update_user_form.cleaned_data
		# group = Group.objects.get(id=data['user_group'])
		profile.name = data["name"]
		if not user.groups.filter(name="Waiter"):
			profile.email = data["email"]
			user.email = data["email"]
			user.username = data["email"]
		
		profile.telephone = data["telephone"]
		user.is_active = data["is_active"]
		profile.save()
		user.save()
		messages.success(request, f"User updated.")
	return redirect('bar:get_profile', id=profile.id)
	

@groups_required("Admin")
@login_required
def update_user_permissions(request, id):
	user = User.objects.filter(id=id).first()
	update_user_permissions_form = UpdateUserPermissionsForm(request.POST)
	if request.method == "POST" and update_user_permissions_form.is_valid():
		def get_true_item(item): 
			if item[1]: return item[0] 
		data = update_user_permissions_form.cleaned_data
		perm_list = list(map(get_true_item ,list(data.items())))
		perms = Permission.objects.filter(codename__in=perm_list).all()
		user.user_permissions.set(perms)
		messages.success(request, "Updated user permissions")
	else:
		print(update_user_permissions_form.errors)
	return redirect('bar:get_profile', id=user.profile.id)


@groups_required("Admin")
@login_required
def update_user_password(request, id):
	user = User.objects.filter(id=id).first()
	update_user_password_form = UpdateUserPasswordForm(request.POST)
	if request.method == "POST" and update_user_password_form.is_valid():
		data = update_user_password_form.cleaned_data
		user.set_password(data["new_password"])
		user.save()
		messages.success(request, "Updated user password")
	else:
		print(update_user_password_form.errors)
	return redirect('bar:get_profile', id=user.profile.id)


@groups_required("Admin")
@login_required
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, f"User deleted")
    return redirect('bar:get_profiles')