from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Order, OrderGroup
from ..utils import STATUS_CHOICES


@login_required
def create_orders(request):
    return render(request, 'pages/create-orders.html')

@login_required
def update_orders(request, order_group_id):
    order_group = OrderGroup.objects.get(id=order_group_id)
    context = {
        "order_group": order_group
    }
    return render(request, 'pages/update-orders.html', context)


@login_required
def orders(request):
    status = request.GET.get("status", 0)
    context = {
        "status": int(status)
    }
    return render(request, 'pages/orders.html', context)


@login_required
def update_order_status(request):
    if request.method == "POST":
        check = request.POST.get("check")
        ref = request.POST.get("ref")
        status = int(request.POST.get("status", 0))
        
        order_group = OrderGroup.objects.get(reference=ref)
        if order_group and status:
            order_group.status = status
            order_group.save()
        
            status_value = dict(STATUS_CHOICES)[status]
            messages.success(request, f"Order {ref} has been marked as {status_value}")
            return redirect(reverse('bar:orders') + f'?status={int(status)-1}')
