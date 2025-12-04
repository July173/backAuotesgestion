from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import Person


class PersonRepository(BaseRepository):
    def __init__(self):
        super().__init__(Person)
