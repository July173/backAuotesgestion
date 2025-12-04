from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models import HumanTalent


class HumanTalentRepository(BaseRepository):
    def __init__(self):
        super().__init__(HumanTalent)
