from django.conf.urls import url, include
from django.http import JsonResponse
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

	def destroy(self, request, *args, **kwargs):
		metric = self.get_object()
		metric_system = metric.metric_system
		if metric_system.base_metric() == metric:
			metric_system.metric_set.all().delete()
		else:
			metric.delete()
		data = MetricSerializer(metric_system.metric_set, many=True).data
		return JsonResponse(data, safe=False)

