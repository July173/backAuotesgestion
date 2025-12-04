from apps.general.entity.serializers.Regional.RegionalSerializer import RegionalSerializer
from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.RegionalRepository import RegionalRepository
from apps.general.entity.models import Regional




class RegionalService(BaseService):
    def create_regional(self, validated_data):
        name = validated_data.get('name', '').strip()
        if not name:
            return None, "El nombre es requerido."
        from apps.general.entity.models.Regional import Regional
        exists = Regional.objects.filter(name__iexact=name, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe una regional con ese nombre."
        serializer = RegionalSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors

    def __init__(self):
        self.repository = RegionalRepository()

    def get_filtered_regionals(self, active=None, search=None):        
        queryset = Regional.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_regional_with_centers_by_id(self, pk):
        """Obtiene una regional por ID con sus centros anidados"""
        try:
            return Regional.objects.prefetch_related('centers').get(pk=pk)
        except Regional.DoesNotExist:
            return None

    def get_all_regionals_with_centers(self):
        """Obtiene todas las regionales con sus centros anidados"""
        return Regional.objects.prefetch_related('centers').all()
