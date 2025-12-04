from rest_framework import serializers
from apps.security.entity.models.DocumentType import DocumentType

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'acronyms', 'active']