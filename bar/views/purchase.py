from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Purchase
from ..forms import FilterPurchasesForm

@login_required
def get_purchases(request):
	query = Purchase.objects
	filter_purchases_form = FilterPurchasesForm(data=request.GET)
	if filter_purchases_form.is_valid():
		data = filter_purchases_form.cleaned_data
		date_lte = data.get("date_lte")
		date_gte = data.get("date_gte")
		product = data.get("product")
		if date_lte:
			query = query.filter(created_at__lte=date_lte)
		if date_gte:
			query = query.filter(created_at__gte=date_gte)
		if product:
			query = query.filter(product_id=product)
	purchases = query.order_by("-created_at").all()
	context = {
		"purchases": purchases,
		"total": sum([purchase.quantity*purchase.purchase_price for purchase in purchases]),
		"filter_purchases_form": filter_purchases_form
	}
	return render(request, 'purchase/purchases.html', context)