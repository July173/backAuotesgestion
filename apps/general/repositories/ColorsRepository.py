from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models.Colors import Colors

class ColorsRepository(BaseRepository):
    """
    Repositorio para operaciones CRUD sobre Colors.
    """
    def __init__(self):
        super().__init__(Colors)
