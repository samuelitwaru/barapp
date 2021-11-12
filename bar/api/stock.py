from django.conf.urls import url, include
from ..models import Stock
from rest_framework import routers, serializers, viewsets



class StockSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Stock
		fields = '__all__'


# ViewSets define the view behavior.
class StockViewSet(viewsets.ModelViewSet):
	queryset = Stock.objects.all()
	serializer_class = StockSerializer