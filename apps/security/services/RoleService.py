# apps/security/services/role_service.py
from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.RoleRepository import RoleRepository
from apps.security.entity.serializers.RoleSerializer import RoleSerializer


class RoleService(BaseService):
    def create_role(self, validated_data):
        from apps.security.entity.models import Role
        name = validated_data.get('type_role', '').strip()
        if not name:
            return None, "El nombre es requerido."
        exists = Role.objects.filter(type_role__iexact=name, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un rol con ese nombre."
        serializer = RoleSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors
    def get_filtered_roles(self, active=None, search=None):
        return self.repository.get_filtered_roles(active, search)
    def __init__(self):
        self.repository = RoleRepository()
    
    def set_active_role_and_users(self, role_id, active):
        """
        Delegar activación/desactivación al repository.
        """
        return self.repository.set_active_role_and_users(role_id, active)

    def list_roles(self):
        """
        Delegar listado al repository.
        """
        return self.repository.list_roles()

    def roles_with_user_count(self):
        """
        Delegar conteo al repository.
        """
        return self.repository.roles_with_user_count()
    