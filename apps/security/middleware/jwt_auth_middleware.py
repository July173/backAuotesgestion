from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser


class JwtAuthMiddleware(BaseMiddleware):
    """ASGI middleware for Channels that authenticates users via a SimpleJWT
    access token passed in the querystring as `?token=...` or in the
    Authorization header as `Bearer <token>`.

    On success it sets `scope['user']` to the Django user instance. On
    failure it sets `scope['user']` to AnonymousUser.
    """

    def __init__(self, inner):
        super().__init__(inner)
        self.jwt_auth = JWTAuthentication()

    async def __call__(self, scope, receive, send):
        # Try querystring first
        token = None
        try:
            qs = parse_qs(scope.get('query_string', b'').decode())
            token = qs.get('token', [None])[0]
        except Exception:
            token = None

        # If no token in querystring, try Authorization header
        if not token:
            headers = dict(scope.get('headers', []))
            auth_header = headers.get(b'authorization')
            if auth_header:
                try:
                    auth_text = auth_header.decode()
                    if auth_text.startswith('Bearer '):
                        token = auth_text.split(' ', 1)[1]
                except Exception:
                    token = None

        if token:
            try:
                # Validate token and retrieve user
                validated_token = self.jwt_auth.get_validated_token(token)
                user = await sync_to_async(self.jwt_auth.get_user)(validated_token)
                scope['user'] = user
            except Exception:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
