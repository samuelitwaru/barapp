from django.conf.urls import url, include
from ..models import Metric
from rest_framework import routers, serializers, viewsets



class MetricSerializer(serializers.ModelSerializer):
	class Meta:
		model = Metric
		fields = '__all__'


# ViewSets define the view behavior.
class MetricViewSet(viewsets.ModelViewSet):
	queryset = Metric.objects.all()
	serializer_class = MetricSerializer

	def get_queryset(self, *args, **kwargs):
		metric_system = int(self.request.GET.get("metric_system", 0))
		queryset = Metric.objects
		if metric_system:
			queryset = queryset.filter(metric_system=metric_system)
		return queryset.all()