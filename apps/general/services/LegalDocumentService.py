from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.LegalDocumentRepository import LegalDocumentRepository
from apps.general.entity.models.LegalDocument import LegalDocument
from django.utils import timezone
from apps.general.entity.serializers.LegalDocumentSerializer import LegalDocumentSerializer


class LegalDocumentService(BaseService):
    def create_legal_document(self, validated_data):
        title = validated_data.get('title', '').strip()
        if not title:
            return None, "El título es requerido."
        exists = LegalDocument.objects.filter(title__iexact=title, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un documento legal con ese título."
        serializer = LegalDocumentSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors

    def __init__(self):
        self.repository = LegalDocumentRepository()

    def get_filtered_legal_documents(self, active=None, search=None):
        queryset = LegalDocument.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset
    def update(self, id, data):
        
        data['last_update'] = timezone.now().date()
        return super().update(id, data)
