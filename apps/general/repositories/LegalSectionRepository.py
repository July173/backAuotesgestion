from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models.LegalSection import LegalSection

class LegalSectionRepository(BaseRepository):
    def __init__(self):
        super().__init__(LegalSection)