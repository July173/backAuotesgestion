from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models.SupportContact import SupportContact

class SupportContactRepository(BaseRepository):
    def __init__(self):
        super().__init__(SupportContact)
