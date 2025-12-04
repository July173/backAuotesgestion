from rest_framework import serializers
from apps.general.entity.models.TypeOfQueries import TypeOfQueries

class TypeOfQueriesSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TypeOfQueries.
    """
    class Meta:
        model = TypeOfQueries
        fields = ['id', 'name', 'description', 'active']
