from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Purchase
from ..forms import FilterPurchasesForm

@login_required
def get_purchases(request):
	filter_purchases_form = FilterPurchasesForm()
	purchases = Purchase.objects.order_by("-created_at").all()
	context = {
		"purchases": purchases,
		"filter_purchases_form": filter_purchases_form
	}
	return render(request, 'purchase/purchases.html', context)