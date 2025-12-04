from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models.SupportSchedule import SupportSchedule

class SupportScheduleRepository(BaseRepository):
    def __init__(self):
        super().__init__(SupportSchedule)
