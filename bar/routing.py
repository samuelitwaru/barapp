from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
	# (?# re_path(r'ws/bar/(?P<room_name>\w+)/$', consumers.BarConsumer.as_asgi()),)
	re_path(r'ws/bar/', consumers.BarConsumer.as_asgi()),
]