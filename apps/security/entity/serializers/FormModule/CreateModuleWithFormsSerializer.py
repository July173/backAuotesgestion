from rest_framework import serializers

class CreateModuleWithFormsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    form_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="Lista de IDs de formularios a asociar al módulo."
    )
