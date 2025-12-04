from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.DocumentTypeRepository import DocumentTypeRepository
from apps.security.entity.models.DocumentType import DocumentType
from apps.security.entity.serializers.DocumentTypeSerializer import DocumentTypeSerializer


class DocumentTypeService(BaseService):
    def get_filtered_document_types(self, active=None, search=None):
        queryset = DocumentType.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def __init__(self):
        super().__init__(DocumentTypeRepository())

    def create_document_type(self, validated_data):
        name = validated_data.get('name', '').strip()
        if not name:
            return None, "El nombre es requerido."
        exists = DocumentType.objects.filter(name__iexact=name, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un tipo de documento con ese nombre."
        serializer = DocumentTypeSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors
