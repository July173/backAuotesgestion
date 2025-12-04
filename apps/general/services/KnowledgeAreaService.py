from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.KnowledgeAreaRepository import KnowledgeAreaRepository
from apps.general.entity.models.KnowledgeArea import KnowledgeArea
from apps.general.entity.serializers.KnowledgeAreaSerializer import KnowledgeAreaSerializer


class KnowledgeAreaService(BaseService):
    def create_knowledge_area(self, validated_data):
        name = validated_data.get('name', '').strip()
        if not name:
            return None, "El nombre es requerido."        
        exists = KnowledgeArea.objects.filter(name__iexact=name, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un área de conocimiento con ese nombre."
        serializer = KnowledgeAreaSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors

    def get_filtered_knowledge_areas(self, active=None, search=None):
        queryset = KnowledgeArea.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def __init__(self):
        self.repository = KnowledgeAreaRepository()
