from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import User, Role
from django.db import transaction


class RoleRepository(BaseRepository):    
    def get_filtered_roles(self, active=None, search=None):
        queryset = self.model.objects.all()
        if active is not None:
            queryset = queryset.filter(active=active)
        if search:
            queryset = queryset.filter(type_role__icontains=search)
        return list(queryset)
    
    def __init__(self):
        super().__init__(Role)
        
    def list_roles(self):
        """
        Devuelve todos los roles.
        """
        return self.model.objects.all()

    def set_active_role_and_users(self, role_id, active):
        """
        Activa o desactiva el rol y todos los usuarios vinculados a ese rol.
        """
        
        with transaction.atomic():
            role = Role.objects.get(pk=role_id)
            role.active = active
            role.save()
            users = User.objects.filter(role_id=role_id)
            users.update(is_active=active)
        estado = "activados" if active else "desactivados"
        return {"detail": f"Rol y usuarios {estado} correctamente."}

    def roles_with_user_count(self):
        """
        Lista roles con cantidad de usuarios activos asignados.
        """
        roles = self.model.objects.all()
        data = []
        for role in roles:
            user_count = User.objects.filter(role=role, is_active=True).count()
            data.append({
                "id": role.id,
                "nombre": role.type_role,
                "descripcion": role.description,
                "active": role.active,
                "cantidad_usuarios": user_count
            })
        return data
    
