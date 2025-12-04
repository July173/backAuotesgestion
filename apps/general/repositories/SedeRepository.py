from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Sede


class SedeRepository(BaseRepository):
    def __init__(self):
        super().__init__(Sede)
