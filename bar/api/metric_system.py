from django.conf.urls import url, include
from django.db import transaction
from rest_framework.decorators import action
from ..models import MetricSystem
from rest_framework import routers, serializers, viewsets
from .metric import MetricSerializer


class MetricSystemSerializer(serializers.ModelSerializer):
	metrics = MetricSerializer(source="metric_set", many=True)
	class Meta:
		model = MetricSystem
		fields = ("id", "created_at", "updated_at", "name", "is_standard", "metrics")


# ViewSets define the view behavior.
class MetricSystemViewSet(viewsets.ModelViewSet):
	queryset = MetricSystem.objects.order_by('-created_at').all()
	serializer_class = MetricSystemSerializer
