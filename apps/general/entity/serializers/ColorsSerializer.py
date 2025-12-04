from rest_framework import serializers
from apps.general.entity.models.Colors import Colors

class ColorsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Colors model.
    """
    class Meta:
        model = Colors
        fields = ['id', 'name', 'hexagonal_value', 'active']
