from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Purchase


@login_required
def get_purchases(request):
	purchases = Purchase.objects.order_by("-created_at").all()
	context = {
		"purchases": purchases
	}
	return render(request, 'purchase/purchases.html', context)