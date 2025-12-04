from apps.security.entity.models import RoleFormPermission
from rest_framework import serializers


class RoleFormPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleFormPermission
        fields = ['id', 'role', 'form', 'permission']
