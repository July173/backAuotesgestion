from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Center


class CenterRepository(BaseRepository):
    def __init__(self):
        super().__init__(Center)

    def get_center_with_sedes_by_id(self, pk):
        """Obtiene un centro por ID con sus sedes anidadas"""
        try:
            return self.model.objects.prefetch_related('sedes').get(pk=pk)
        except self.model.DoesNotExist:
            return None

    def get_all_centers_with_sedes(self):
        """Obtiene todos los centros con sus sedes anidadas"""
        return self.model.objects.prefetch_related('sedes').all()
    
