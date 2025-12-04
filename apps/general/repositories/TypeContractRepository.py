from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models.TypeContract import TypeContract

class TypeContractRepository(BaseRepository):
    def __init__(self):
        super().__init__(TypeContract)
