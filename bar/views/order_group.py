from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect 
from django.contrib import messages
from ..models import OrderGroup
from ..forms import FilterOrderGroupsForm
from ..utils import STATUS_CHOICES


@login_required
def get_order_groups(request):
    # date_lte = request.GET.get("date_lte")
    # date_gte = request.GET.get("date_gte")
    query = OrderGroup.objects
    
    filter_order_groups_form = FilterOrderGroupsForm(data=request.GET)
    if filter_order_groups_form.is_valid():
        data = filter_order_groups_form.cleaned_data
        date_lte = data.get("date_lte")
        date_gte = data.get("date_gte")
        status = data.get("status")
        if date_lte:
            query = query.filter(created_at__lte=date_lte)
        if date_gte:
            query = query.filter(created_at__gte=date_gte)
        print(">>>>>>>>", status)
        if isinstance(status, bool):
            print("dooooooooo", status)
            query = query.filter(closed=status)


    order_groups = query.order_by("-created_at").all()
    context = {
        "order_groups": order_groups,
        "filter_order_groups_form": filter_order_groups_form
    }
    return render(request, 'order_group/order-groups.html', context)
    

@login_required
def get_order_group(request, id):
    order_group = OrderGroup.objects.get(id=id)
    context = {
        "order_group": order_group,
        "orders": order_group.order_set.all()
    }
    return render(request, "order_group/order-group.html", context)


@login_required
def open_or_close_order_group(request, id):
    order_group = OrderGroup.objects.get(id=id)
    order_group.closed = not order_group.closed
    status = "OPENED"
    if order_group.closed: status = "CLOSED"
    messages.success(request, f"Order {status}")
    order_group.save()
    next = request.META.get('HTTP_REFERER', None) or '/'
    return HttpResponseRedirect(next)


@login_required
def delete_order_group(request, id):
    order_group = OrderGroup.objects.get(id=id)
    ref = order_group.reference
    order_group.delete()
    messages.success(request, f"Deleted order {ref}")
    return redirect('bar:orders')