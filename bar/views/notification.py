from datetime import datetime
from django.db.models import F
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.http import JsonResponse
from ..models import Product, Order, OrderGroup
from bar.api import ProductSerializer, OrderGroupSerializer


class Notification:

	def __init__(self, title, description, url, tag=""):
		self.title = title
		self.description = description
		self.url = url
		self.tag = tag


@login_required
def get_notifications(request):
	# low stock products
	low_stock_products = Product.objects.filter(quantity__lte=F("stock_limit")).all()
	# pending orders
	pending_orders = OrderGroup.objects.filter(status=0).all()
	# ready orders
	ready_orders = OrderGroup.objects.filter(status=1).all()
	notifications = []
	for order_group in pending_orders:
		notification = Notification("Pending Order", f"The {order_group} is pending", reverse("bar:orders"))
		notifications.append(notification)

	for order_group in ready_orders:
		notification = Notification("Ready Order", f"The {order_group} is ready", reverse("bar:orders")+"?status=1")
		notifications.append(notification)
	for product in low_stock_products:
		notification = Notification("Low Stock", f"The {product} has low stock", f"/products/{product.id}", tag="danger")
		notifications.append(notification)

	context = {
		"notifications": notifications,
		"count": len(notifications)
	}
	return render(request, 'notification/notifications.html', context)


	# res = [
	# 	{
	# 		"message": f"{len(low_stock_products)} Product(s) with low stock!",
	# 		"items": low_stock_products,
	# 		"url": reverse("bar:get_products")
	# 	}, 
	# 	{
	# 		"message": f"{len(pending_orders)} Pending Orders",
	# 		"items":pending_orders,
	# 		"url": reverse("bar:orders")
	# 	}, 
	# 	{
	# 		"message": f"{len(ready_orders)} Ready Orders",
	# 		"items":ready_orders,
	# 		"url": reverse("bar:orders")+"?status=1"
	# 	}, 
	# ]
	# return JsonResponse(res, safe=False)


@login_required
def get_notification_count(request):
	# low stock products
	low_stock_products = Product.objects.filter(quantity__lte=F("stock_limit")).count()
	# pending orders
	pending_orders = OrderGroup.objects.filter(status=0).count()
	# ready orders
	ready_orders = OrderGroup.objects.filter(status=1).count()
	return JsonResponse({"count":low_stock_products+pending_orders+ready_orders})


