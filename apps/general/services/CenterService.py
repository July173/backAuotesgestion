from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.CenterRepository import CenterRepository
from apps.general.entity.models import Center
from apps.general.entity.serializers.CenterSerializer import CenterSerializer


class CenterService(BaseService):
    def create_center(self, validated_data):
        name = validated_data.get('name', '').strip()
        if not name:
            return None, "El nombre es requerido."
        exists = Center.objects.filter(name__iexact=name, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un centro con ese nombre."
        serializer = CenterSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors

    def __init__(self):
        self.repository = CenterRepository()

    def get_filtered_centers(self, active=None, search=None):
        queryset = Center.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_center_with_sedes_by_id(self, pk):
        """Delegar la consulta al repository."""
        return self.repository.get_center_with_sedes_by_id(pk)

    def get_all_centers_with_sedes(self):
        """Delegar la consulta al repository."""
        return self.repository.get_all_centers_with_sedes()
