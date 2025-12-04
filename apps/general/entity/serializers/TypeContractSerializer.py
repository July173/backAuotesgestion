from rest_framework import serializers
from apps.general.entity.models.TypeContract import TypeContract

class TypeContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeContract
        fields = ['id', 'name', 'description', 'active']