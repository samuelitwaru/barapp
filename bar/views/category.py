from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, DetailView
from ..models import Category
from ..forms import CreateCategoryForm, DeleteCategoryForm, UpdateCategoryForm


def create_category(request):
	create_category_form = CreateCategoryForm()
	if request.method=="POST":
		create_category_form = CreateCategoryForm(request.POST)
		if create_category_form.is_valid():
			data = create_category_form.cleaned_data
			category = Category.objects.create(**data)
			messages.success(request, "Category created")
			return redirect('bar:get_products')
	context = {
		"create_category_form": create_category_form
	}
	return render(request, 'category/create-category.html', context)


def get_category(request, id):
	category = Category.objects.get(id=id)
	update_category_form = UpdateCategoryForm(data={
		"name": category.name
		}, category=category)
	if request.method=="POST":
		update_category_form = UpdateCategoryForm(data=request.POST, category=category)
		if update_category_form.is_valid():
			data = update_category_form.cleaned_data
			category.name = data["name"]
			category.save()
			messages.success(request, "Category updated")
			return redirect('bar:get_products')
	context = {
		"update_category_form": update_category_form,
		"category": category
	}
	return render(request, 'category/category.html', context)


def delete_category(request, id):
	category = Category.objects.get(id=id)
	delete_category_form = DeleteCategoryForm()
	if request.method=="POST":
		create_category_form = DeleteCategoryForm(request.POST)
		if create_category_form.is_valid():
			category.delete()
			messages.success(request, "Category deleted")
	return redirect('bar:get_products')
