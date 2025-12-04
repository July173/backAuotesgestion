from rest_framework import serializers

class FormRequestSerializer(serializers.Serializer):
    """
    Serializer for form requests. All help texts remain in Spanish for user-facing documentation.
    """
    # IDs to link existing entities
    apprentice = serializers.IntegerField(help_text="ID del aprendiz")
    ficha = serializers.IntegerField(help_text="ID de la ficha")

    # Data created in the request
    fecha_inicio_contrato = serializers.DateField(help_text="Fecha de inicio de contrato de aprendizaje", required=False, allow_null=True)
    fecha_fin_contrato = serializers.DateField(help_text="Fecha de fin de contrato de aprendizaje", required=False, allow_null=True)
    enterprise_name = serializers.CharField(max_length=100, help_text="Nombre de la empresa")
    enterprise_nit = serializers.CharField(max_length=100, help_text="NIT de la empresa (solo números)")
    enterprise_location = serializers.CharField(max_length=255, help_text="Ubicación de la empresa")
    enterprise_email = serializers.EmailField(help_text="Correo electrónico de la empresa")
    boss_name = serializers.CharField(max_length=100, help_text="Nombre del jefe inmediato")
    boss_phone = serializers.IntegerField(help_text="Teléfono del jefe (solo números)")
    boss_email = serializers.EmailField(help_text="Correo del jefe inmediato")
    boss_position = serializers.CharField(max_length=100, help_text="Cargo del jefe inmediato")
    human_talent_name = serializers.CharField(max_length=100, help_text="Nombre del responsable de talento humano")
    human_talent_email = serializers.EmailField(help_text="Correo de talento humano")
    human_talent_phone = serializers.IntegerField(help_text="Teléfono de talento humano (solo números)")
    sede = serializers.IntegerField(help_text="ID de la sede")
    modality_productive_stage = serializers.IntegerField(help_text="ID de la modalidad de etapa productiva")
