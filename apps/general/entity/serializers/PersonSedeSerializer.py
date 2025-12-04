from apps.general.entity.models import PersonSede, Sede
from apps.security.entity.models import Person
from rest_framework import serializers


class PersonSedeSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for foreign keys
    sede = serializers.PrimaryKeyRelatedField(queryset=Sede.objects.all(), required=True)
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), required=True)

    class Meta:
        model = PersonSede
        fields = [
            'id',
            'sede',
            'person',
            'active',
        ]
