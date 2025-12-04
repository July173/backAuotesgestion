from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models.KnowledgeArea import KnowledgeArea


class KnowledgeAreaRepository(BaseRepository):
    def __init__(self):
        super().__init__(KnowledgeArea)
