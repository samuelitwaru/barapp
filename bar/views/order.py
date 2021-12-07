from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from ..models import Order, OrderGroup
from ..forms import FilterOrderGroupsForm, FilterOrdersForm
from ..utils import STATUS_CHOICES



@login_required
def create_orders(request):
    return render(request, 'pages/create-orders.html')


@login_required
def orders(request):
    status = request.GET.get("status", 0)
    filter_orders_form = FilterOrderGroupsForm(v_model=True)
    context = {
        "status": int(status),
        "filter_orders_form": filter_orders_form
    }
    return render(request, 'pages/orders.html', context)


@login_required
def update_order_status(request):
    if request.method == "POST":
        check = request.POST.get("check")
        ref = request.POST.get("ref")
        status = int(request.POST.get("status", 0))
        
        order = OrderGroup.objects.get(reference=ref)
        if order and status:
            order.status = status
            order.save()
        
            status_value = dict(STATUS_CHOICES)[status]
            messages.success(request, f"Order {ref} has been marked as {status_value}")
            return redirect(reverse('bar:orders') + f'?status={int(status)-1}')



@login_required
def get_order_sales(request):
    query = Order.objects
    filter_orders_form = FilterOrdersForm(data=request.GET)
    if filter_orders_form.is_valid():
        data = filter_orders_form.cleaned_data
        date_lte = data.get("date_lte")
        date_gte = data.get("date_gte")
        product = data.get("product")
        if date_lte:
            query = query.filter(created_at__lte=date_lte)
        if date_gte:
            query = query.filter(created_at__gte=date_gte)
        if product:
            query = query.filter(product_id=product)
    orders = query.order_by("-created_at").all()
    page = int(request.GET.get("page", 1))
    paginator = Paginator(orders, 50)
    orders = paginator.get_page(page)
    context = {
        "orders":orders,
        "count":len(orders),
        "total": sum([order.quantity*order.sale_price for order in orders]),
        "filter_orders_form": filter_orders_form
    }
    return render(request,'order/order-sales.html', context)