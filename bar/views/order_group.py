from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import OrderGroup
from ..utils import STATUS_CHOICES


@login_required
def get_order_group(request, id):
    order_group = OrderGroup.objects.get(id=id)
    context = {
        "order_group": order_group
    }
    return render(request, "order_group/order-group.html", context)


@login_required
def delete_order_group(request, id):
    order_group = OrderGroup.objects.get(id=id)
    ref = order_group.reference
    order_group.delete()
    messages.success(request, f"Deleted order {ref}")
    return redirect('bar:orders')