from rest_framework import serializers

class FormularioPermisoSerializer(serializers.Serializer):
    form_id = serializers.IntegerField()
    permission_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)


class CreateRoleWithPermissionsSerializer(serializers.Serializer):
    type_role = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    active = serializers.BooleanField(default=True)
    # Use 'forms' as the input key to match service expectations
    forms = FormularioPermisoSerializer(many=True)
