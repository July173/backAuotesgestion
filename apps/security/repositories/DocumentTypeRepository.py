from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models.DocumentType import DocumentType

class DocumentTypeRepository(BaseRepository):
    def __init__(self):
        super().__init__(DocumentType)
