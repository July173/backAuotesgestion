from rest_framework import serializers
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer

class RegisterAprendizSerializer(PersonSerializer):
    """
    DTO para el registro de aprendices.
    Solo define los campos necesarios, sin validaciones de negocio.
    """
    
    email = serializers.EmailField(
        required=True,
        help_text="Correo institucional del aprendiz"
    )
    
    class Meta(PersonSerializer.Meta):
        # Incluir email además de todos los campos de PersonSerializer
        fields = PersonSerializer.Meta.fields + ['email']
        ref_name = "RegisterAprendizSerializer"