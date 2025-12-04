# apps/security/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importa los ViewSets de todas las tablas
from apps.security.views.UserViewset import UserViewSet
from apps.security.views.RoleViewset import RoleViewSet
from apps.security.views.PersonViewset import PersonViewSet
from apps.security.views.FormViewset import FormViewSet
from apps.security.views.PermissionViewset import PermissionViewSet
from apps.security.views.ModuleViewset import ModuleViewSet
from apps.security.views.FormModuleViewset import FormModuleViewSet
from apps.security.views.RoleFormPermissionViewset import RoleFormPermissionViewSet
from apps.security.views.ExcelTemplateViewSet import ExcelTemplateViewSet
from apps.security.views.auth_viewset import LoginView, RefreshView
from apps.security.views.DocumentTypeViewset import DocumentTypeViewset

# Configura el router y registra todos los ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'persons', PersonViewSet, basename='persons')
router.register(r'forms', FormViewSet, basename='forms')
router.register(r'permissions', PermissionViewSet, basename='permissions')
router.register(r'modules', ModuleViewSet, basename='modules')
router.register(r'form-modules', FormModuleViewSet, basename='form-modules')
router.register(r'rol-form-permissions', RoleFormPermissionViewSet, basename='rol-form-permissions')
router.register(r'excel-templates', ExcelTemplateViewSet, basename='excel-templates')
router.register(r'document-types', DocumentTypeViewset, basename='document-types')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),  # Incluir las rutas del router
]
