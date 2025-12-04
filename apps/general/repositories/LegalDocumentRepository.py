from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models.LegalDocument import LegalDocument

class LegalDocumentRepository(BaseRepository):
    def __init__(self):
        super().__init__(LegalDocument)
