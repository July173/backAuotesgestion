from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:
    def login(self, email, password):
        user = authenticate(email=email, password=password)
        if not user:
            return None
        refresh = RefreshToken.for_user(user)
        # Obtener el campo person, asumiendo que user.person existe
        person = None
        if hasattr(user, 'person'):
            # Si es una relación, puedes serializar el objeto o solo el id
            try:
                person = user.person.id
            except Exception:
                person = None
                print('user:', user, 'person:', person)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role.id if hasattr(user, 'role') else None,
                'person': person
            }
        }
    