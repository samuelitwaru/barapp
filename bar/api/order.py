from django.conf.urls import url, include
from django.db import transaction
from ..models import Order, OrderGroup, SaleGuide, Product
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
		orders = request.data.get("orders")
		customer = request.data.get("customer")
		ref = generate_order_ref()
		order_group = OrderGroup(reference=ref, waiter_id=request.user.id, customer=customer)
		order_group.save()
		for product in orders:
			sale_guide = SaleGuide.objects.get(id=product.get("orderSaleGuide").get("id"))
			sale_guide_metric = sale_guide.metric
			order_quantity = product.get("orderQuantity")
			order = Order(
				reference=ref,
				quantity=order_quantity,
				product_name=product.get("name"),
				purchase_price=product.get("purchase_price"),
				purchase_metric=product.get("purchase_metric").get("unit"),
				sale_price=sale_guide.price,
				sale_metric=sale_guide_metric.unit,
				order_group = order_group,
				product_id=product.get("id"),
				sale_guide_id=sale_guide.id,
			)
			product = Product.objects.get(id=product.get("id"))
			product.update_quantity_by(0-order_quantity, sale_guide_metric)
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
			sale_guide = SaleGuide.objects.get(id=product.get("orderSaleGuide").get("id"))
			sale_guide_metric = sale_guide.metric
			order_quantity = product.get("orderQuantity")
			
			order = order_group.order_set.filter(product_id=product["id"]).first()
			product_obj = Product.objects.get(id=product.get("id"))

			if order:
				current_quantity = order.quantity
				current_sale_guide = order.sale_guide

				if order_quantity!=current_quantity or sale_guide!=current_sale_guide:
					# revert product quantity
					product_obj.update_quantity_by(current_quantity, current_sale_guide.metric)
					# update order
					order.quantity = order_quantity
					order.sale_guide = sale_guide
					order.save()
					product_obj.update_quantity_by(0-order_quantity, sale_guide.metric)
			else:
				order = Order(
					reference=order_group.reference,
					quantity=order_quantity,
					product_name=product.get("name"),
					purchase_price=product.get("purchase_price"),
					purchase_metric=product.get("purchase_metric").get("unit"),
					sale_price=sale_guide.price,
					sale_metric=sale_guide_metric.unit,
					order_group = order_group,
					product_id=product.get("id"),
					sale_guide_id=sale_guide.id,
				)
				order.save()
				product_obj.update_quantity_by(0-order_quantity, sale_guide_metric)
			new_order_ids.append(order.id)
		
		# delete all orders that have been removed
		orders_to_remove = order_group.order_set.exclude(id__in=new_order_ids)
		for order in orders_to_remove.all():
			product = order.product
			sale_guide = SaleGuide.objects.get(product_id=product.id)
			sale_guide_metric = sale_guide.metric
			if product:
				product.update_quantity_by(order.quantity, sale_guide_metric)
			order.delete()

		success_response = {
			"status": "success",
			"data": order_group_api.OrderGroupSerializer(order_group).data
		}
		return JsonResponse(success_response)


	@action(detail=False, methods=['post'])
	def update_order_status(self, request):
		ref = request.data.get("ref")
		status = request.data.get("status")
		order_group = OrderGroup.objects.get(reference=ref)
		if order_group and status:
			order_group.update(status=status)
		else:
			response = {
				"status": "failure",
				"detail": "Bad Request"
			}
		return JsonResponse(response)