from apps.general.entity.models.KnowledgeArea import KnowledgeArea
from rest_framework import serializers


class KnowledgeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeArea
        fields = [
            'id',
            'name',
            'description',
            'active'
        ]
