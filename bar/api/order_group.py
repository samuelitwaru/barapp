from django.conf.urls import url, include
from ..models import OrderGroup
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from ..utils import generate_order_ref
from ..forms import FilterOrderGroupsForm
from . import order



class OrderGroupSerializer(serializers.ModelSerializer):
	orders = order.OrderSerializer(source="order_set", many=True, read_only=True)
	waiter = serializers.CharField(read_only=True)
	class Meta:
		model = OrderGroup
		fields = "__all__"
		fields = ("id", "reference", "created_at", "updated_at", "closed", "status", "waiter", "customer", "orders",)
		read_only_fields = ("reference",)


# ViewSets define the view behavior.
class OrderGroupViewSet(viewsets.ModelViewSet):
	queryset = OrderGroup.objects.order_by("-created_at").all()
	serializer_class = OrderGroupSerializer

	def get_queryset(self, *args, **kwargs):
		filter_order_groups_form = FilterOrderGroupsForm(data=self.request.GET)
		queryset = OrderGroup.objects
		if filter_order_groups_form.is_valid():
			data = filter_order_groups_form.cleaned_data
			date_lte = data.get("date_lte")
			date_gte = data.get("date_gte")
			waiter = data.get("waiter")
			status = data.get("status")
			if date_lte:
				queryset = queryset.filter(created_at__lte=date_lte)
			if date_gte:
				queryset = queryset.filter(created_at__gte=date_gte)
			if waiter:
				queryset = queryset.filter(waiter_id=waiter)
			if isinstance(status, bool):
				queryset = queryset.filter(closed=status)
		return queryset.all()