from django.conf.urls import url, include
from rest_framework.response import Response
from ..models import SaleGuide
from rest_framework import routers, serializers, viewsets
from .metric import MetricSerializer



class SaleGuideSerializer(serializers.ModelSerializer):
	metric = MetricSerializer(read_only=True)
	metric_id = serializers.IntegerField(source="metric.id")
	class Meta:
		model = SaleGuide
		fields = ("id", "metric", "price", "metric_id", "product")

	# def create(self, validated_data):
	# 	print(">>> ", validated_data)


# ViewSets define the view behavior.
class SaleGuideViewSet(viewsets.ModelViewSet):
	queryset = SaleGuide.objects.all()
	serializer_class = SaleGuideSerializer

	def get_queryset(self, *args, **kwargs):
		product = int(self.request.GET.get("product", 0))
		queryset = SaleGuide.objects
		if product:
			queryset = queryset.filter(product=product)
		return queryset.all()

	def create(self, request):
		metric = request.data["metric_id"]
		price = request.data["price"]
		product = request.data["product"]
		sale_guide = SaleGuide.objects.create(metric_id=metric, price=price, product_id=product)
		return Response(SaleGuideSerializer(sale_guide).data)