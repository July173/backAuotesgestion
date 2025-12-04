from apps.general.entity.models import Apprentice, Ficha
from apps.security.entity.models import Person
from rest_framework import serializers


class ApprenticeSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for foreign keys
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), required=True)
    ficha = serializers.PrimaryKeyRelatedField(queryset=Ficha.objects.all(), required=True)

    class Meta:
        model = Apprentice
        fields = [
            'id',
            'person',
            'ficha',
            'active'
        ]
