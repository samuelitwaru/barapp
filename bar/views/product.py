from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import F
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from ..models import Product, Category, Product
from ..forms import UpdateProductForm, UpdateProductPurchasingForm, CreateProductForm, CreateCategoryForm, UpdateProductCategoriesForm, AddProductStockForm, FilterProductsForm
from ..decorators import *


class ProductsPageView(TemplateView):
	template_name = "product/products.html"

	def get_context_data(self, ** kwargs):
		context = super().get_context_data(**kwargs)
		create_category_form = CreateCategoryForm()
		context['products'] = Product.objects.all()
		low_stock_products = Product.objects.filter(quantity__lte=F("stock_limit")).all()
		if low_stock_products:
			messages.error(self.request, f"{len(low_stock_products)} Product(s) with low stock!", extra_tags="danger")
		context['categories'] = Category.objects.all()
		return context


@groups_required("Admin", "Cashier")
@login_required
def get_products(request):
	query = Product.objects
	filter_products_form = FilterProductsForm(data=request.GET)
	if filter_products_form.is_valid():
		data = filter_products_form.cleaned_data
		metric_system = data.get("metric_system")
		category = data.get("category")
		if metric_system:
			query = query.filter(metric_system_id=metric_system)
		if category:
			query = query.filter(categories__id=category)
	
	categories = Category.objects.all()
	products = query.all()
	page = int(request.GET.get("page", 1))
	p = Paginator(products, 50)
	products = p.get_page(page)
	context = {
		"products": products,
		"categories": categories,
		"filter_products_form": filter_products_form
	}
	return render(request, 'product/products.html', context)

@groups_required("Admin", "Cashier")
@login_required
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


@groups_required("Admin", "Cashier")
@login_required
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
	if request.method=="POST":
		update_product_form = UpdateProductForm(data=request.POST, product=product)
		if update_product_form.is_valid():
			data = update_product_form.cleaned_data
			product.name = data["name"]
			product.brand = data["brand"]
			product.barcode = data["barcode"]
			product.description = data["description"]
			product.barcode = data["barcode"]
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


@groups_required("Admin", "Cashier")
@login_required
def update_product_purchasing(request, id):
	product = Product.objects.filter(id=id).first()
	update_product_purchasing_form = UpdateProductPurchasingForm(data=request.POST, product=product)
	if request.method=="POST" and update_product_purchasing_form.is_valid():
		data = update_product_purchasing_form.cleaned_data
		old_purchase_metric = product.purchase_metric
		new_purchase_metric = data["purchase_metric"]
		new_purchase_price = data["purchase_price"]

		if old_purchase_metric and old_purchase_metric != new_purchase_metric:
			product.convert_quantities(old_purchase_metric, new_purchase_metric)
		
		product.purchase_metric = new_purchase_metric
		product.purchase_price = new_purchase_price
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


@groups_required("Admin", "Cashier")
@login_required
def update_product_categories(request, id):
	product = Product.objects.filter(id=id).first()
	update_product_categories_form = UpdateProductCategoriesForm(data=request.POST)
	if request.POST and update_product_categories_form.is_valid():
		data = update_product_categories_form.cleaned_data
		product.categories.set(data["categories"])
		product.save()
		messages.success(request, "Product categories updated")
	return redirect('bar:get_product', id=product.id)


@groups_required("Admin", "Cashier")
@login_required
def add_product_stock(request, id):
	product = Product.objects.filter(id=id).first()
	add_product_stock_form = AddProductStockForm(data={
		"quantity": 1,
		"purchase_metric": getattr(product.purchase_metric, "id", None),
		"purchase_price": product.purchase_price,
		}, product=product)
	if request.method=="POST":
		add_product_stock_form = AddProductStockForm(data=request.POST, product=product)
		if add_product_stock_form.is_valid():
			data = add_product_stock_form.cleaned_data
			old_purchase_metric = product.purchase_metric
			new_purchase_metric = data["purchase_metric"]
			new_purchase_price = data["purchase_price"]
			quantity = data["quantity"]
			if old_purchase_metric and old_purchase_metric != new_purchase_metric:
				product.convert_quantities(old_purchase_metric, new_purchase_metric)

			product.purchase_metric = new_purchase_metric
			product.purchase_price = new_purchase_price
			product.quantity += quantity
			product.save()
			# Product.objects.create(product_name=product.name, purchase_price=new_purchase_price, 
			# 	purchase_metric=new_purchase_metric.unit, quantity=quantity, product_id=product.id
			# 	)
			messages.success(request, "Product stock added")
			return redirect('bar:get_product', id=product.id)

	context = {
		"product": product,
		"add_product_stock_form": add_product_stock_form,
	}
	return render(request, 'product/add-product-stock.html', context)