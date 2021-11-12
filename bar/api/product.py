from django.conf.urls import url, include
from ..models import Product
from rest_framework import routers, serializers, viewsets
from .sale_guide import SaleGuideSerializer
from .metric import MetricSerializer



class ProductSerializer(serializers.ModelSerializer):
	sale_guides = SaleGuideSerializer(many=True)
	purchase_metric = MetricSerializer()
	class Meta:
		model = Product
		fields = ("id","created_at","updated_at","name","brand","description","barcode","quantity","purchase_price","metric_system","purchase_metric","categories", "sale_guides")


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer