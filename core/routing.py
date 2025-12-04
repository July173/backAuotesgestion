from channels.routing import URLRouter
from channels.security.websocket import OriginValidator, AllowedHostsOriginValidator
import apps.general.routing
from apps.security.middleware.jwt_auth_middleware import JwtAuthMiddleware

# Expose a websocket ASGI application (not a ProtocolTypeRouter). The top-level
# ProtocolTypeRouter will be created in core.asgi, combining HTTP and websocket.
# Adjust allowed_origins for your frontend hosts/ports.
allowed_origins = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

websocket_application = AllowedHostsOriginValidator(
    OriginValidator(
        # Use JwtAuthMiddleware which sets `scope['user']` from a SimpleJWT
        # access token passed via `?token=` or Authorization header.
        JwtAuthMiddleware(
            URLRouter(apps.general.routing.websocket_urlpatterns)
        ),
        allowed_origins
    )
)

# Note: core.asgi will import `websocket_application` and combine it with the
# django ASGI application under a ProtocolTypeRouter.
