from datetime import datetime
from django.db.models import F
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.http import JsonResponse
from ..models import Product, Order, OrderGroup
from bar.api import ProductSerializer, OrderGroupSerializer


@login_required
def get_notifications(request):
	# low stock products
	low_stock_products = Product.objects.filter(quantity__lte=F("stock_limit")).all()
	low_stock_products = ProductSerializer(low_stock_products, many=True).data
	# pending orders
	pending_orders = OrderGroup.objects.filter(status=0).all()
	# print(pending_orders)
	pending_orders = OrderGroupSerializer(pending_orders, many=True).data
	# ready orders
	ready_orders = OrderGroup.objects.filter(status=1).all()
	ready_orders = OrderGroupSerializer(ready_orders, many=True).data

	res = [
		{
			"message": f"{len(low_stock_products)} Products have low stock!",
			"items": low_stock_products,
			"url": reverse("bar:get_products")
		}, 
		{
			"message": "Pending Orders",
			"items":pending_orders,
			"url": reverse("bar:orders")
		}, 
		{
			"message": "Pending Orders",
			"items":ready_orders,
			"url": reverse("bar:orders")
		}, 
	]
	return JsonResponse(res, safe=False)


