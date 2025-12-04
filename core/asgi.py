
import os
# Ensure DJANGO_SETTINGS_MODULE is set before importing any Django/ASGI modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

django_asgi_app = get_asgi_application()

# Import routing after Django apps are initialized to avoid AppRegistryNotReady
import core.routing

application = ProtocolTypeRouter({
	"http": django_asgi_app,
	"websocket": core.routing.websocket_application,
})
