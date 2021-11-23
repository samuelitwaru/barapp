from bar.models import *


order_groups = {}


def create_order_groups():
	print("starting...")
	order_group = None
	for order in Order.objects.all():
		if not order_groups.get(order.reference):
			order_groups[order.reference] = []
			order_group = OrderGroup(reference=order.reference)
			order_group.save()
		order_groups[order.reference].append(order)
		order.order_group = order_group
		order.save()
	print(order_groups)

