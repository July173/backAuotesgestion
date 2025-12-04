from rest_framework import serializers
from apps.assign.entity.models import Enterprise


class EnterpriseSerializer(serializers.ModelSerializer):
    nit_enterprise = serializers.IntegerField(default=92233720360)  # Valor por defecto

    class Meta:
        model = Enterprise
        fields = [
            'id',
            'name_enterprise',
            'locate',
            'nit_enterprise',
            'active',
            'email_enterprise'
        ]
