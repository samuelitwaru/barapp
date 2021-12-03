from django.conf.urls import url, include
from ..models import Product
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import routers, serializers, viewsets
from .sale_guide import SaleGuideSerializer
from .metric import MetricSerializer



class ProductSerializer(serializers.ModelSerializer):
	sale_guides = SaleGuideSerializer(many=True)
	purchase_metric = MetricSerializer()
	class Meta:
		model = Product
		fields = ("id","created_at","updated_at","name","brand","description","barcode","quantity","stock_limit","purchase_price","metric_system","purchase_metric","categories", "sale_guides")


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

	@action(detail=True, methods=['put'])
	@transaction.atomic
	def update_stock_limit(self, request, pk):
		stock_limit = request.data.get("stock_limit")		
		product = Product.objects.get(id=pk)
		product.stock_limit = stock_limit
		product.save()
		return JsonResponse(ProductSerializer(product).data)
