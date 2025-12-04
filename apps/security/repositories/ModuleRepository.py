from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import Module


class ModuleRepository(BaseRepository):
    def get_filtered_modules(self, active=None, search=None):
        queryset = self.model.objects.all()
        if active is not None:
            queryset = queryset.filter(active=active)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return list(queryset)
    def __init__(self):
        super().__init__(Module)
