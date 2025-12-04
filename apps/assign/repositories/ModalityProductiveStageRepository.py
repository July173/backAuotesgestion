from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models import ModalityProductiveStage


class ModalityProductiveStageRepository(BaseRepository):
    def __init__(self):
        super().__init__(ModalityProductiveStage)
