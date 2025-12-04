from apps.general.entity.models import Regional
from rest_framework import serializers


class RegionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regional
        fields = [
            'id',
            'name',
            'code_regional',
            'description',
            'active',
            'address'
        ]
