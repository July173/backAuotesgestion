from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginView(TokenObtainPairView):
    serializer_class=TokenObtainPairSerializer
    permission_classes=[permissions.AllowAny]
    
class RefreshView(TokenRefreshView):
    permission_classes=[permissions.AllowAny]
