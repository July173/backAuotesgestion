from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.LegalSectionRepository import LegalSectionRepository
from apps.general.entity.models.LegalSection import LegalSection
from apps.general.entity.serializers.LegalSectionSerializer import LegalSectionSerializer


class LegalSectionService(BaseService):
    def create_legal_section(self, validated_data):
        title = validated_data.get('title', '').strip()
        if not title:
            return None, "El título es requerido."
        exists = LegalSection.objects.filter(title__iexact=title, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe una sección legal con ese título."        
        serializer = LegalSectionSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors

    def __init__(self):
        super().__init__(LegalSectionRepository())

    def get_filtered_legal_sections(self, active=None, search=None):        
        queryset = LegalSection.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset