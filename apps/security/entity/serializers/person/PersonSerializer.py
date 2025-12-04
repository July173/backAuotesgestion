from rest_framework import serializers
from apps.security.entity.models import Person

from apps.security.entity.models.DocumentType import DocumentType

class PersonSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_null=True, required=False)
    # PrimaryKeyRelatedField maneja automáticamente la conversión ID <-> Objeto
    type_identification = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.filter(active=True)
    )

    class Meta:
        model = Person
        fields = [
            'id',
            'first_name',
            'second_name',
            'first_last_name',
            'second_last_name',
            'phone_number',
            'type_identification',
            'number_identification',
            'active',
            'image'
        ]
        ref_name = "PersonModelSerializer"
