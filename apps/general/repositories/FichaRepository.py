from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Ficha


class FichaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Ficha)
