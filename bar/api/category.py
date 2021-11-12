from django.conf.urls import url, include
from ..models import Category
from rest_framework import routers, serializers, viewsets



class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = "__all__"


# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer