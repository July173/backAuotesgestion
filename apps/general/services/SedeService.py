from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.SedeRepository import SedeRepository
from apps.general.entity.models.Sede import Sede
from apps.general.entity.serializers.SedeSerializer import SedeSerializer

class SedeService(BaseService):
    def create_sede(self, validated_data):
        name = validated_data.get('name', '').strip()
        if not name:
            return None, "El nombre es requerido."
        exists = Sede.objects.filter(name__iexact=name, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe una sede con ese nombre."        
        serializer = SedeSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors
    def __init__(self):
        self.repository = SedeRepository()

    def get_filtered_sedes(self, active=None, search=None):        
        queryset = Sede.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
