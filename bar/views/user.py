from django.views.generic import TemplateView, DetailView
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from ..models import User, Profile
from ..forms import UpdateUserPermissionsForm, UpdateUserForm, CreateUserForm, UpdateUserPasswordForm


# class UsersPageView(TemplateView):
# 	template_name = "user/users.html"

# 	def get_context_data(self, ** kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context['users'] = User.objects.all()
# 		return context


# class UserDetailView(DetailView):
# 	model = User
# 	template_name = "user/user.html"



def create_user(request):
	create_user_form = CreateUserForm()
	if request.method=="POST":
		create_user_form = CreateUserForm(request.POST)
		if create_user_form.is_valid():
			data = create_user_form.cleaned_data
			user = User.objects.create(username=data["email"], email=data["email"])
			user.set_password(data["password"])
			user.save()
			profile = Profile.objects.create(name=data["name"], email=data["email"], telephone=data["telephone"], user=user)
			messages.success(request, "User created")
			return redirect('bar:update_user', id=user.id)

	context = {
		"create_user_form": create_user_form
	}
	return render(request, 'profile/create-profile.html', context)



@login_required
def update_user(request, id):
	user = User.objects.filter(id=id).first()
	profile = user.profile

	update_user_form = UpdateUserForm(data=request.POST, profile=profile)
	if request.method == "POST" and update_user_form.is_valid():
		data = update_user_form.cleaned_data
		profile.name = data["name"]
		profile.email = data["email"]
		profile.telephone = data["telephone"]
		user.email = data["email"]
		user.username = data["email"]
		user.is_active = data["is_active"]
		profile.save()
		user.save()
		messages.success(request, f"User updated.")
	return redirect('bar:get_profile', id=profile.id)
	

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


