from django.conf.urls import url, include
from ..models import Profile
from rest_framework import routers, serializers, viewsets



class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = '__all__'


# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ModelViewSet):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer