# mysite/asgi.py
import os
import django
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
import bar.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bar_project.settings')

application = ProtocolTypeRouter({
	"http": AsgiHandler(),
	"websocket": AuthMiddlewareStack(
		URLRouter(
			bar.routing.websocket_urlpatterns
		)
	),
})