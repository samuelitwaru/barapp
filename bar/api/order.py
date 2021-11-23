from django.conf.urls import url, include
from django.db import transaction
from ..models import Order, OrderGroup
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from ..utils import generate_order_ref
from . import order_group as order_group_api



class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'


# ViewSets define the view behavior.
class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.order_by("-created_at").all()
	serializer_class = OrderSerializer

	@action(detail=False, methods=['post'])
	@transaction.atomic
	def create_orders(self, request):
		orders = request.data
		ref = generate_order_ref()
		order_group = OrderGroup(reference=ref, waiter_id=request.user.id)
		order_group.save()
		for product in orders:
			order = Order(
				reference=ref,
				quantity=product.get("orderQuantity"),
				product_name=product.get("name"),
				purchase_price=product.get("purchase_price"),
				purchase_metric=product.get("purchase_metric").get("unit"),
				sale_price=product.get("orderSaleGuide").get("price"),
				sale_metric=product.get("orderSaleGuide").get("metric").get("unit"),
				order_group = order_group,
				product_id=product.get("id"),
				sale_guide_id=product.get("orderSaleGuide").get("id"),
			)
			order.save()

		success_response = {
			"status": "success",
			"detail": "Orders were created successfully"
		}
		return JsonResponse(success_response)


	@action(detail=True, methods=['put'])
	@transaction.atomic
	def update_orders(self, request, pk):
		orders = request.data
		order_group = OrderGroup.objects.get(id=pk)
		new_order_ids = []
		for product in orders:
			order = order_group.order_set.filter(product_id=product["id"]).first()
			if order:
				order.quantity = product["orderQuantity"]
			else:
				order = Order(
					reference=order_group.reference,
					quantity=product.get("orderQuantity"),
					product_name=product.get("name"),
					purchase_price=product.get("purchase_price"),
					purchase_metric=product.get("purchase_metric").get("unit"),
					sale_price=product.get("orderSaleGuide").get("price"),
					sale_metric=product.get("orderSaleGuide").get("metric").get("unit"),
					order_group = order_group,
					product_id=product.get("id"),
					sale_guide_id=product.get("orderSaleGuide").get("id"),
				)
			order.save()
			new_order_ids.append(order.id)
		order_group.order_set.exclude(id__in=new_order_ids).delete()
		# order_group.save()

		success_response = {
			"status": "success",
			"data": order_group_api.OrderGroupSerializer(order_group).data
		}
		return JsonResponse(success_response)


	@action(detail=False, methods=['post'])
	def update_order_status(self, request):
		ref = request.data.get("ref")
		status = request.data.get("status")
		if ref and status:
			orders = Order.objects.filter(reference=ref)
			orders.update(reference=ref, status=status)
			response = {
				"status": "success",
				"detail": "Action successful."
			}
		else:
			response = {
				"status": "failure",
				"detail": "Bad Request"
			}
		return JsonResponse(response)