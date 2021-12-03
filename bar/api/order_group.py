from django.conf.urls import url, include
from ..models import OrderGroup
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from ..utils import generate_order_ref
from . import order



class OrderGroupSerializer(serializers.ModelSerializer):
	orders = order.OrderSerializer(source="order_set", many=True, read_only=True)
	waiter = serializers.CharField(source="waiter.profile")
	class Meta:
		model = OrderGroup
		fields = "__all__"
		fields = ("id", "reference", "created_at", "updated_at", "closed", "status", "customer", "waiter", "orders",)
		read_only_fields = ("reference",)


# ViewSets define the view behavior.
class OrderGroupViewSet(viewsets.ModelViewSet):
	queryset = OrderGroup.objects.order_by("-created_at").all()
	serializer_class = OrderGroupSerializer