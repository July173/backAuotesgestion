from rest_framework import serializers
from apps.general.entity.models.LegalDocument import LegalDocument

class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = ['id', 'type', 'title', 'effective_date', 'active']
