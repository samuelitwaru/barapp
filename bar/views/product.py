from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, DetailView
from ..models import Product, Category
from ..forms import UpdateProductForm, UpdateProductPurchasingForm, CreateProductForm, CreateCategoryForm, UpdateProductCategoriesForm


class ProductsPageView(TemplateView):
	template_name = "product/products.html"

	def get_context_data(self, ** kwargs):
		context = super().get_context_data(**kwargs)
		create_category_form = CreateCategoryForm()
		context['products'] = Product.objects.all()
		context['categories'] = Category.objects.all()
		return context


def create_product(request):
	create_product_form = CreateProductForm()
	if request.method=="POST":
		create_product_form = CreateProductForm(request.POST)
		if create_product_form.is_valid():
			data = create_product_form.cleaned_data
			product = Product.objects.create(**data)
			messages.success(request, "Product created")
			return redirect('bar:get_product', id=product.id)

	context = {
		"create_product_form": create_product_form
	}
	return render(request, 'product/create-product.html', context)


def get_product(request, id):
	product = Product.objects.filter(id=id).first()
	categories = Category.objects.all()
	update_product_categories_form = UpdateProductCategoriesForm(categories=categories, product=product)
	update_product_form = UpdateProductForm(data={
			"name": product.name,
			"brand": product.brand,
			"description": product.description,
			"barcode": product.barcode,
			"quantity": product.quantity,
			"metric_system": product.metric_system.id
		}, product=product)
	if request.method=="POST" and update_product_form.is_valid():
		data = update_product_form.cleaned_data
		product.name = data["name"]
		product.brand = data["brand"]
		product.barcode = data["barcode"]
		product.description = data["description"]
		product.barcode = data["barcode"]
		# product.quantity = data["quantity"]
		product.metric_system = data["metric_system"]
		product.save()
		messages.success(request, "Product updated")
		return redirect('bar:get_product', id=product.id)

	update_product_purchasing_form = UpdateProductPurchasingForm(data={
		"purchase_metric": getattr(product.purchase_metric, "id", None),
		"purchase_price": product.purchase_price,
	}, product=product)
	context = {
		"object": product,
		"update_product_form": update_product_form,
		"update_product_categories_form": update_product_categories_form,
		"update_product_purchasing_form": update_product_purchasing_form,

	}
	return render(request, 'product/product.html', context)


def update_product_purchasing(request, id):
	product = Product.objects.filter(id=id).first()
	update_product_purchasing_form = UpdateProductPurchasingForm(data=request.POST, product=product)
	if request.method=="POST" and update_product_purchasing_form.is_valid():
		data = update_product_purchasing_form.cleaned_data
		product.purchase_metric = data["purchase_metric"]
		product.purchase_price = data["purchase_price"]
		product.save()
		messages.success(request, "Product purchasing updated")
		return redirect('bar:get_product', id=product.id)

	update_product_form = UpdateProductForm(data={
		"name": product.name,
		"brand": product.brand,
		"description": product.description,
		"barcode": product.barcode,
		"metric_system": product.metric_system.id,
	}, product=product)
	context = {
		"object": product,
		"update_product_form": update_product_form,
		"update_product_purchasing_form": update_product_purchasing_form,
	}
	return render(request, 'product/product.html', context)


def update_product_categories(request, id):
	product = Product.objects.filter(id=id).first()
	update_product_categories_form = UpdateProductCategoriesForm(data=request.POST)
	if request.POST and update_product_categories_form.is_valid():
		data = update_product_categories_form.cleaned_data
		product.categories.set(data["categories"])
		product.save()
		messages.success(request, "Product categories updated")
	return redirect('bar:get_product', id=product.id)