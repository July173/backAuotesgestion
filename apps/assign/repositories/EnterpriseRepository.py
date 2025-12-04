from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models import Enterprise


class EnterpriseRepository(BaseRepository):
    def __init__(self):
        super().__init__(Enterprise)
