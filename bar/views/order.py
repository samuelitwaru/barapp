from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Order
from ..utils import STATUS_CHOICES


@login_required
def create_orders(request):
    return render(request, 'pages/create-orders.html')


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
        if check and ref and status:
            orders = Order.objects.filter(reference=ref)
            orders.update(reference=ref, status=status, updated_at=datetime.now())
        
        status_value = dict(STATUS_CHOICES)[status]
        messages.success(request, f"Order {ref} has been marked as {status_value}")
        return redirect(reverse('bar:orders') + f'?status={int(status)-1}')
